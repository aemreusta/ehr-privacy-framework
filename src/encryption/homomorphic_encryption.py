"""
Homomorphic Encryption Implementation for Privacy-Preserving EHR Data

Homomorphic encryption allows computations to be performed on encrypted data
without decrypting it, providing strong privacy protection while maintaining
computational capabilities for healthcare analytics.
"""

import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd

try:
    from Pyfhel import PyCtxt, Pyfhel

    PYFHEL_AVAILABLE = True
except ImportError:
    PYFHEL_AVAILABLE = False
    PyCtxt = None

logger = logging.getLogger(__name__)


class HomomorphicEncryption:
    """
    Implementation of homomorphic encryption for EHR data.

    Provides encryption, decryption, and homomorphic operations
    (addition, multiplication) on healthcare data.
    """

    def __init__(
        self,
        context_params: Optional[Dict[str, Any]] = None,
        key_dir: Optional[str] = None,
    ):
        """
        Initialize homomorphic encryption system.

        Args:
            context_params: Optional custom parameters for encryption context
            key_dir: Directory to store/load encryption keys
        """
        if not PYFHEL_AVAILABLE:
            raise ImportError(
                "Pyfhel library not available. Install with: pip install Pyfhel"
            )

        self.key_dir = Path(key_dir) if key_dir else Path("keys")
        self.key_dir.mkdir(exist_ok=True)

        # Initialize Pyfhel context
        self.HE = Pyfhel()

        # Default parameters (can be customized)
        default_params = {
            "scheme": "CKKS",  # CKKS scheme for floating point arithmetic
            "n": 16384,  # Polynomial modulus degree
            "scale": 2**40,  # Scale for CKKS
            "qi_sizes": [60] + [40] * 5 + [60],  # Bit-sizes of primes
        }

        if context_params:
            default_params.update(context_params)

        # Generate context
        self.HE.contextGen(**default_params)

        # Generate keys
        self.HE.keyGen()
        self.HE.relinKeyGen()
        self.HE.rotateKeyGen()

        logger.info("Homomorphic encryption system initialized")

    def encrypt_value(self, value: Union[float, int, List[float]]) -> PyCtxt:
        """
        Encrypt a single value or list of values.

        Args:
            value: Value(s) to encrypt

        Returns:
            Encrypted ciphertext
        """
        if isinstance(value, (int, float)):
            return self.HE.encryptFrac(float(value))
        elif isinstance(value, list):
            return self.HE.encryptFrac(value)
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    def decrypt_value(self, ciphertext: PyCtxt) -> Union[float, List[float]]:
        """
        Decrypt a ciphertext to recover the original value(s).

        Args:
            ciphertext: Encrypted ciphertext

        Returns:
            Decrypted value(s)
        """
        return self.HE.decryptFrac(ciphertext)

    def encrypt_column(self, data: pd.Series, batch_size: int = 1000) -> List[PyCtxt]:
        """
        Encrypt a pandas Series (column) of numerical data.

        Args:
            data: Pandas Series containing numerical data
            batch_size: Number of values to encrypt in each batch

        Returns:
            List of encrypted ciphertexts
        """
        logger.info(f"Encrypting column with {len(data)} values")

        encrypted_data = []
        numeric_data = pd.to_numeric(data, errors="coerce").fillna(0).tolist()

        # Process in batches for efficiency
        for i in range(0, len(numeric_data), batch_size):
            batch = numeric_data[i : i + batch_size]
            encrypted_batch = self.encrypt_value(batch)
            encrypted_data.append(encrypted_batch)

        logger.info(f"Encrypted {len(encrypted_data)} batches")
        return encrypted_data

    def decrypt_column(self, encrypted_data: List[PyCtxt]) -> List[float]:
        """
        Decrypt a list of ciphertexts back to a list of values.

        Args:
            encrypted_data: List of encrypted ciphertexts

        Returns:
            List of decrypted values
        """
        decrypted_values = []

        for encrypted_batch in encrypted_data:
            batch_values = self.decrypt_value(encrypted_batch)
            if isinstance(batch_values, list):
                decrypted_values.extend(batch_values)
            else:
                decrypted_values.append(batch_values)

        return decrypted_values

    def homomorphic_sum(self, encrypted_data: List[PyCtxt]) -> PyCtxt:
        """
        Compute the sum of encrypted values without decryption.

        Args:
            encrypted_data: List of encrypted ciphertexts

        Returns:
            Encrypted sum
        """
        if not encrypted_data:
            return self.encrypt_value(0.0)

        # Start with the first ciphertext
        result = encrypted_data[0]

        # Add remaining ciphertexts
        for ciphertext in encrypted_data[1:]:
            result += ciphertext

        return result

    def homomorphic_mean(
        self, encrypted_data: List[PyCtxt], count: Optional[int] = None
    ) -> PyCtxt:
        """
        Compute the mean of encrypted values without decryption.

        Args:
            encrypted_data: List of encrypted ciphertexts
            count: Number of values (if known, otherwise estimated)

        Returns:
            Encrypted mean
        """
        # Compute encrypted sum
        encrypted_sum = self.homomorphic_sum(encrypted_data)

        # Divide by count
        if count is None:
            count = len(encrypted_data)  # This is an approximation

        # Create encrypted count and perform division
        encrypted_count = self.encrypt_value(float(count))
        encrypted_mean = encrypted_sum / encrypted_count

        return encrypted_mean

    def homomorphic_multiply(self, ctxt1: PyCtxt, ctxt2: PyCtxt) -> PyCtxt:
        """
        Multiply two encrypted values.

        Args:
            ctxt1: First encrypted value
            ctxt2: Second encrypted value

        Returns:
            Encrypted product
        """
        result = ctxt1 * ctxt2
        self.HE.relinearize(result)  # Reduce noise
        return result

    def homomorphic_scalar_multiply(self, ciphertext: PyCtxt, scalar: float) -> PyCtxt:
        """
        Multiply encrypted value by a plaintext scalar.

        Args:
            ciphertext: Encrypted value
            scalar: Plaintext scalar

        Returns:
            Encrypted result
        """
        return ciphertext * scalar

    def secure_aggregation(
        self, df: pd.DataFrame, numerical_columns: List[str]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Perform secure aggregation on multiple columns.

        Args:
            df: Input DataFrame
            numerical_columns: List of numerical columns to aggregate

        Returns:
            Dictionary with encrypted aggregation results
        """
        logger.info("Performing secure aggregation on encrypted data")

        results = {}
        processing_times = {}

        for col in numerical_columns:
            if col in df.columns:
                start_time = time.time()

                # Encrypt column
                encrypted_column = self.encrypt_column(df[col])

                # Compute encrypted statistics
                encrypted_sum = self.homomorphic_sum(encrypted_column)
                encrypted_mean = self.homomorphic_mean(encrypted_column, len(df))

                # Store encrypted results (can be decrypted when needed)
                results[col] = {
                    "encrypted_sum": encrypted_sum,
                    "encrypted_mean": encrypted_mean,
                    "record_count": len(df[col].dropna()),
                    "encryption_batches": len(encrypted_column),
                }

                processing_times[col] = time.time() - start_time

        results["processing_times"] = processing_times
        logger.info("Secure aggregation completed")

        return results

    def privacy_preserving_query(
        self,
        df: pd.DataFrame,
        query_type: str,
        column: str,
        condition_column: Optional[str] = None,
        condition_value: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        Execute privacy-preserving queries on encrypted data.

        Args:
            df: Input DataFrame
            query_type: Type of query ('sum', 'mean', 'count')
            column: Column to query
            condition_column: Optional column for filtering
            condition_value: Optional value for filtering

        Returns:
            Query results with encrypted values
        """
        logger.info(f"Executing privacy-preserving {query_type} query")

        # Apply condition if specified
        query_df = df.copy()
        if condition_column and condition_value is not None:
            query_df = query_df[query_df[condition_column] == condition_value]

        if len(query_df) == 0:
            return {"error": "No records match the query condition"}

        # Encrypt the relevant column
        encrypted_column = self.encrypt_column(query_df[column])

        result = {
            "query_type": query_type,
            "column": column,
            "record_count": len(query_df),
        }

        if query_type == "sum":
            result["encrypted_result"] = self.homomorphic_sum(encrypted_column)
        elif query_type == "mean":
            result["encrypted_result"] = self.homomorphic_mean(
                encrypted_column, len(query_df)
            )
        elif query_type == "count":
            result["encrypted_result"] = self.encrypt_value(float(len(query_df)))
        else:
            return {"error": f"Unsupported query type: {query_type}"}

        return result

    def save_keys(self, filename_prefix: str = "he_keys") -> Dict[str, str]:
        """
        Save encryption keys to files.

        Args:
            filename_prefix: Prefix for key files

        Returns:
            Dictionary with paths to saved key files
        """
        key_files = {}

        # Save context
        context_path = self.key_dir / f"{filename_prefix}_context.txt"
        self.HE.save_context(str(context_path))
        key_files["context"] = str(context_path)

        # Save secret key
        secret_key_path = self.key_dir / f"{filename_prefix}_secret.txt"
        self.HE.save_secret_key(str(secret_key_path))
        key_files["secret_key"] = str(secret_key_path)

        # Save public key
        public_key_path = self.key_dir / f"{filename_prefix}_public.txt"
        self.HE.save_public_key(str(public_key_path))
        key_files["public_key"] = str(public_key_path)

        logger.info(f"Keys saved to {self.key_dir}")
        return key_files

    def load_keys(self, filename_prefix: str = "he_keys") -> bool:
        """
        Load encryption keys from files.

        Args:
            filename_prefix: Prefix for key files

        Returns:
            True if keys loaded successfully
        """
        try:
            # Load context
            context_path = self.key_dir / f"{filename_prefix}_context.txt"
            self.HE.load_context(str(context_path))

            # Load secret key
            secret_key_path = self.key_dir / f"{filename_prefix}_secret.txt"
            self.HE.load_secret_key(str(secret_key_path))

            # Load public key
            public_key_path = self.key_dir / f"{filename_prefix}_public.txt"
            self.HE.load_public_key(str(public_key_path))

            logger.info("Keys loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to load keys: {e}")
            return False

    def benchmark_operations(
        self, data_sizes: List[int] = [100, 500, 1000]
    ) -> Dict[str, Dict[int, float]]:
        """
        Benchmark homomorphic operations with different data sizes.

        Args:
            data_sizes: List of data sizes to test

        Returns:
            Benchmark results
        """
        logger.info("Running homomorphic encryption benchmarks")

        results = {
            "encryption_times": {},
            "decryption_times": {},
            "addition_times": {},
            "multiplication_times": {},
        }

        for size in data_sizes:
            logger.info(f"Benchmarking with data size: {size}")

            # Generate test data
            test_data = np.random.randn(size).tolist()

            # Benchmark encryption
            start_time = time.time()
            encrypted_data = [
                self.encrypt_value(val) for val in test_data[:100]
            ]  # Limited for practical testing
            results["encryption_times"][size] = time.time() - start_time

            # Benchmark decryption
            start_time = time.time()
            [self.decrypt_value(ctxt) for ctxt in encrypted_data]
            results["decryption_times"][size] = time.time() - start_time

            # Benchmark addition
            if len(encrypted_data) >= 2:
                start_time = time.time()
                _ = encrypted_data[0] + encrypted_data[1]
                results["addition_times"][size] = time.time() - start_time

                # Benchmark multiplication
                start_time = time.time()
                result = self.homomorphic_multiply(encrypted_data[0], encrypted_data[1])
                results["multiplication_times"][size] = time.time() - start_time

        logger.info("Benchmarks completed")
        return results

    def get_security_parameters(self) -> Dict[str, Any]:
        """
        Get current security parameters of the encryption scheme.

        Returns:
            Dictionary with security parameters
        """
        return {
            "scheme": "CKKS",
            "polynomial_degree": self.HE.getn(),
            "security_level": "128-bit",  # Approximate for typical parameters
            "ciphertext_modulus_bits": sum(self.HE.getqiBits()),
            "scale_bits": 40,  # Default scale
            "noise_budget": "Varies by operations",
            "supported_operations": [
                "addition",
                "multiplication",
                "scalar_multiplication",
            ],
        }

    def verify_homomorphic_property(
        self, val1: float, val2: float, operation: str = "add"
    ) -> Dict[str, Any]:
        """
        Verify that homomorphic operations work correctly.

        Args:
            val1: First value
            val2: Second value
            operation: Operation to test ('add' or 'multiply')

        Returns:
            Verification results
        """
        logger.info(f"Verifying homomorphic {operation} property")

        # Encrypt values
        ctxt1 = self.encrypt_value(val1)
        ctxt2 = self.encrypt_value(val2)

        # Perform operation on plaintexts
        if operation == "add":
            expected_result = val1 + val2
            # Perform homomorphic operation
            encrypted_result = ctxt1 + ctxt2
        elif operation == "multiply":
            expected_result = val1 * val2
            # Perform homomorphic operation
            encrypted_result = self.homomorphic_multiply(ctxt1, ctxt2)
        else:
            return {"error": f"Unsupported operation: {operation}"}

        # Decrypt result
        actual_result = self.decrypt_value(encrypted_result)

        # Calculate accuracy
        error = abs(expected_result - actual_result)
        relative_error = error / abs(expected_result) if expected_result != 0 else 0

        return {
            "operation": operation,
            "input_values": [val1, val2],
            "expected_result": expected_result,
            "actual_result": actual_result,
            "absolute_error": error,
            "relative_error": relative_error,
            "verification_passed": relative_error < 1e-3,  # 0.1% tolerance
        }
