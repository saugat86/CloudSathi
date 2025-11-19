import React from 'react';
import { AlertCircle, XCircle } from 'lucide-react';

interface ErrorAlertProps {
    message: string;
    onDismiss?: () => void;
}

const ErrorAlert: React.FC<ErrorAlertProps> = ({ message, onDismiss }) => {
    return (
        <div className="rounded-lg bg-red-50 border border-red-200 p-4">
            <div className="flex items-start">
                <AlertCircle className="h-5 w-5 text-red-600 mt-0.5" />
                <div className="ml-3 flex-1">
                    <h3 className="text-sm font-medium text-red-800">Error</h3>
                    <p className="mt-1 text-sm text-red-700">{message}</p>
                </div>
                {onDismiss && (
                    <button
                        onClick={onDismiss}
                        className="ml-3 text-red-600 hover:text-red-800"
                    >
                        <XCircle className="h-5 w-5" />
                    </button>
                )}
            </div>
        </div>
    );
};

export default ErrorAlert;
