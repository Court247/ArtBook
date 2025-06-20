// src/components/Spinner.jsx
export default function Spinner() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <svg className="animate-spin h-10 w-10 text-blue-500" viewBox="0 0 24 24">
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
          fill="none"
        />
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8v8z"
        />
      </svg>
    </div>
  );
}
