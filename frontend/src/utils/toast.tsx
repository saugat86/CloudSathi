import { useState } from 'react';

export function useToast() {
  const [toast, setToast] = useState<string | null>(null);
  function showToast(msg: string) {
    setToast(msg);
    setTimeout(() => setToast(null), 3000);
  }
  function Toast() {
    return toast ? (
      <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-red-600 text-white px-4 py-2 rounded shadow-lg z-50">
        {toast}
      </div>
    ) : null;
  }
  return { showToast, Toast };
}
