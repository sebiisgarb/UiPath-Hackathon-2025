import { CreditCard, ArrowLeft } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

interface PaymentPageProps {
  onBack: () => void;
}

export function PaymentPage({ onBack }: PaymentPageProps) {
  const { theme } = useTheme();

  return (
    <div className="min-h-screen pt-24 pb-16">
      <div className="max-w-2xl mx-auto px-6">
        <button
          onClick={onBack}
          className={`mb-8 flex items-center gap-2 transition-colors ${
            theme === 'light'
              ? 'text-blue-600 hover:text-blue-700'
              : 'text-cyan-400 hover:text-cyan-300'
          }`}
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Checkout
        </button>

        <div
          className={`rounded-3xl p-12 text-center ${
            theme === 'light'
              ? 'bg-white shadow-xl'
              : 'bg-[#13273F] shadow-2xl shadow-blue-900/30 border border-cyan-500/20'
          }`}
        >
          <div
            className={`w-20 h-20 mx-auto mb-6 rounded-full flex items-center justify-center ${
              theme === 'light'
                ? 'bg-gradient-to-br from-purple-500 to-blue-500'
                : 'bg-gradient-to-br from-cyan-500 to-blue-600 shadow-lg shadow-cyan-500/30'
            }`}
          >
            <CreditCard className="w-10 h-10 text-white" />
          </div>
          <h1
            className={`text-3xl font-bold mb-4 ${
              theme === 'light' ? 'text-gray-800' : 'text-white'
            }`}
          >
            Payment Placeholder
          </h1>
          <p
            className={`text-lg ${
              theme === 'light' ? 'text-gray-600' : 'text-gray-300'
            }`}
          >
            Payment integration would be implemented here.
          </p>
        </div>
      </div>
    </div>
  );
}
