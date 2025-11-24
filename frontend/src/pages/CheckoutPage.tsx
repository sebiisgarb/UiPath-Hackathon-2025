import {
  Plane,
  Hotel,
  Calendar,
  ArrowLeft,
  CreditCard,
  ShieldCheck,
} from "lucide-react";
import { useTheme } from "../context/ThemeContext";
import { Flight, Accommodation } from "../types/trip";
import { useState } from "react";

interface CheckoutPageProps {
  flight: Flight | null;
  hotel: Accommodation | null;
  nights: number;
  destination: string;
  travelDates: string;
  onBack: () => void;
  onProceedToPayment: () => void; // final confirmation / success page
}

export function CheckoutPage({
  flight,
  hotel,
  nights,
  destination,
  travelDates,
  onBack,
  onProceedToPayment,
}: CheckoutPageProps) {
  const { theme } = useTheme();
  const [cardName, setCardName] = useState("");
  const [cardNumber, setCardNumber] = useState("");
  const [expiry, setExpiry] = useState("");
  const [cvv, setCvv] = useState("");
  const [email, setEmail] = useState("");
  const [acceptTerms, setAcceptTerms] = useState(false);
  const [processing, setProcessing] = useState(false);

  const flightPrice = flight?.price || 0;
  const hotelPricePerNight = hotel?.pricePerNight || 0;
  const hotelTotal = hotelPricePerNight * nights;
  const subtotal = flightPrice + hotelTotal;
  const serviceFee = +(subtotal * 0.02).toFixed(2); // 2% serv.
  const taxes = +(subtotal * 0.19).toFixed(2); // TVA 19%
  const grandTotal = (subtotal + serviceFee + taxes).toFixed(2);

  const formValid =
    cardName &&
    cardNumber.replace(/\s+/g, "").length >= 12 &&
    expiry &&
    cvv.length >= 3 &&
    email.includes("@") &&
    acceptTerms &&
    flight &&
    hotel;

  const handlePay = () => {
    if (!formValid) return;
    setProcessing(true);
    setTimeout(() => {
      setProcessing(false);
      onProceedToPayment();
    }, 1200);
  };

  return (
    <div className="min-h-screen pt-24 pb-32">
      <div className="max-w-4xl mx-auto px-6">
        <button
          onClick={onBack}
          className={`mb-8 flex items-center gap-2 transition-colors ${
            theme === "light"
              ? "text-blue-600 hover:text-blue-700"
              : "text-cyan-400 hover:text-cyan-300"
          }`}
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Plan
        </button>

        <div className="mb-8">
          <h1
            className={`text-3xl md:text-4xl font-bold mb-2 ${
              theme === "light" ? "text-gray-800" : "text-white"
            }`}
          >
            Checkout & Plata
          </h1>
          <p
            className={`text-lg ${
              theme === "light" ? "text-gray-600" : "text-gray-300"
            }`}
          >
            Rezumat călătorie + detalii plată securizată
          </p>
        </div>

        <div className="space-y-6 mb-8">
          <div
            className={`rounded-2xl p-6 ${
              theme === "light"
                ? "bg-white shadow-lg"
                : "bg-[#13273F] shadow-lg shadow-blue-900/20 border border-cyan-500/10"
            }`}
          >
            <div className="flex items-center gap-3 mb-4">
              <div
                className={`p-2 rounded-full ${
                  theme === "light"
                    ? "bg-blue-100 text-blue-600"
                    : "bg-cyan-500/20 text-cyan-400"
                }`}
              >
                <Plane className="w-5 h-5" />
              </div>
              <h2
                className={`text-xl font-bold ${
                  theme === "light" ? "text-gray-800" : "text-white"
                }`}
              >
                Zbor Selectat
              </h2>
            </div>
            {flight ? (
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span
                    className={
                      theme === "light" ? "text-gray-600" : "text-gray-300"
                    }
                  >
                    Companie
                  </span>
                  <span
                    className={`font-semibold ${
                      theme === "light" ? "text-gray-800" : "text-white"
                    }`}
                  >
                    {flight.airline}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span
                    className={
                      theme === "light" ? "text-gray-600" : "text-gray-300"
                    }
                  >
                    Plecare
                  </span>
                  <span
                    className={`font-semibold ${
                      theme === "light" ? "text-gray-800" : "text-white"
                    }`}
                  >
                    {flight.originCode} • {flight.departureTime}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span
                    className={
                      theme === "light" ? "text-gray-600" : "text-gray-300"
                    }
                  >
                    Sosire
                  </span>
                  <span
                    className={`font-semibold ${
                      theme === "light" ? "text-gray-800" : "text-white"
                    }`}
                  >
                    {flight.destinationCode} • {flight.arrivalTime}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span
                    className={
                      theme === "light" ? "text-gray-600" : "text-gray-300"
                    }
                  >
                    Durată
                  </span>
                  <span
                    className={`font-semibold ${
                      theme === "light" ? "text-gray-800" : "text-white"
                    }`}
                  >
                    {flight.duration}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span
                    className={
                      theme === "light" ? "text-gray-600" : "text-gray-300"
                    }
                  >
                    Opriri
                  </span>
                  <span
                    className={`font-semibold ${
                      theme === "light" ? "text-gray-800" : "text-white"
                    }`}
                  >
                    {flight.stops}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span
                    className={
                      theme === "light" ? "text-gray-600" : "text-gray-300"
                    }
                  >
                    Bagaj
                  </span>
                  <span
                    className={`font-semibold ${
                      theme === "light" ? "text-gray-800" : "text-white"
                    }`}
                  >
                    {flight.baggage}
                  </span>
                </div>
                <div
                  className={`pt-3 border-t flex justify-between ${
                    theme === "light" ? "border-gray-200" : "border-cyan-500/20"
                  }`}
                >
                  <span
                    className={`font-semibold ${
                      theme === "light" ? "text-gray-800" : "text-white"
                    }`}
                  >
                    Cost zbor
                  </span>
                  <span
                    className={`text-lg font-bold ${
                      theme === "light" ? "text-blue-300" : "text-yellow-300"
                    }`}
                  >
                    €{flightPrice}
                  </span>
                </div>
              </div>
            ) : (
              <p
                className={`text-sm ${
                  theme === "light" ? "text-gray-600" : "text-gray-300"
                }`}
              >
                Niciun zbor selectat.
              </p>
            )}
          </div>

          <div
            className={`rounded-2xl p-6 ${
              theme === "light"
                ? "bg-white shadow-lg"
                : "bg-[#13273F] shadow-lg shadow-blue-900/20 border border-cyan-500/10"
            }`}
          >
            <div className="flex items-center gap-3 mb-4">
              <div
                className={`p-2 rounded-full ${
                  theme === "light"
                    ? "bg-blue-100 text-blue-600"
                    : "bg-cyan-500/20 text-cyan-400"
                }`}
              >
                <Hotel className="w-5 h-5" />
              </div>
              <h2
                className={`text-xl font-bold ${
                  theme === "light" ? "text-gray-800" : "text-white"
                }`}
              >
                Cazare Selectată
              </h2>
            </div>
            {hotel ? (
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span
                    className={
                      theme === "light" ? "text-gray-600" : "text-gray-300"
                    }
                  >
                    Nume
                  </span>
                  <span
                    className={`font-semibold ${
                      theme === "light" ? "text-gray-800" : "text-white"
                    }`}
                  >
                    {hotel.name}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span
                    className={
                      theme === "light" ? "text-gray-600" : "text-gray-300"
                    }
                  >
                    Tip
                  </span>
                  <span
                    className={`font-semibold ${
                      theme === "light" ? "text-gray-800" : "text-white"
                    }`}
                  >
                    {hotel.type}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span
                    className={
                      theme === "light" ? "text-gray-600" : "text-gray-300"
                    }
                  >
                    Perioadă
                  </span>
                  <span
                    className={`font-semibold ${
                      theme === "light" ? "text-gray-800" : "text-white"
                    }`}
                  >
                    {travelDates || "—"}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span
                    className={
                      theme === "light" ? "text-gray-600" : "text-gray-300"
                    }
                  >
                    Nopți
                  </span>
                  <span
                    className={`font-semibold ${
                      theme === "light" ? "text-gray-800" : "text-white"
                    }`}
                  >
                    {nights}
                  </span>
                </div>
                <div
                  className={`pt-3 border-t flex justify-between ${
                    theme === "light" ? "border-gray-200" : "border-cyan-500/20"
                  }`}
                >
                  <span
                    className={`font-semibold ${
                      theme === "light" ? "text-gray-800" : "text-white"
                    }`}
                  >
                    Cost cazare
                  </span>
                  <span
                    className={`text-lg font-bold ${
                      theme === "light" ? "text-blue-300" : "text-yellow-300"
                    }`}
                  >
                    €{hotelTotal}
                  </span>
                </div>
              </div>
            ) : (
              <p
                className={`text-sm ${
                  theme === "light" ? "text-gray-600" : "text-gray-300"
                }`}
              >
                Nicio cazare selectată.
              </p>
            )}
          </div>

          <div
            className={`rounded-2xl p-6 ${
              theme === "light"
                ? "bg-white shadow-lg"
                : "bg-[#13273F] shadow-lg shadow-blue-900/20 border border-cyan-500/10"
            }`}
          >
            <div className="flex items-center gap-3 mb-4">
              <div
                className={`p-2 rounded-full ${
                  theme === "light"
                    ? "bg-blue-100 text-blue-600"
                    : "bg-cyan-500/20 text-cyan-400"
                }`}
              >
                <Calendar className="w-5 h-5" />
              </div>
              <h2
                className={`text-xl font-bold ${
                  theme === "light" ? "text-gray-800" : "text-white"
                }`}
              >
                Rezumat & Cost
              </h2>
            </div>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span
                  className={
                    theme === "light" ? "text-gray-600" : "text-gray-300"
                  }
                >
                  Destinație
                </span>
                <span
                  className={`font-medium ${
                    theme === "light" ? "text-gray-800" : "text-white"
                  }`}
                >
                  {destination || "—"}
                </span>
              </div>
              <div className="flex justify-between">
                <span
                  className={
                    theme === "light" ? "text-gray-600" : "text-gray-300"
                  }
                >
                  Perioadă
                </span>
                <span
                  className={`font-medium ${
                    theme === "light" ? "text-gray-800" : "text-white"
                  }`}
                >
                  {travelDates || "—"}
                </span>
              </div>
              <div className="flex justify-between">
                <span
                  className={
                    theme === "light" ? "text-gray-600" : "text-gray-300"
                  }
                >
                  Subtotal
                </span>
                <span
                  className={`font-semibold ${
                    theme === "light" ? "text-gray-800" : "text-white"
                  }`}
                >
                  €{subtotal}
                </span>
              </div>
              <div className="flex justify-between">
                <span
                  className={
                    theme === "light" ? "text-gray-600" : "text-gray-300"
                  }
                >
                  Taxe (19%)
                </span>
                <span
                  className={`font-semibold ${
                    theme === "light" ? "text-gray-800" : "text-white"
                  }`}
                >
                  €{taxes}
                </span>
              </div>
              <div className="flex justify-between">
                <span
                  className={
                    theme === "light" ? "text-gray-600" : "text-gray-300"
                  }
                >
                  Servicii (2%)
                </span>
                <span
                  className={`font-semibold ${
                    theme === "light" ? "text-gray-800" : "text-white"
                  }`}
                >
                  €{serviceFee}
                </span>
              </div>
              <div
                className={`pt-3 border-t flex justify-between ${
                  theme === "light" ? "border-gray-200" : "border-cyan-500/20"
                }`}
              >
                <span
                  className={`font-bold ${
                    theme === "light" ? "text-gray-800" : "text-white"
                  }`}
                >
                  Total
                </span>
                <span
                  className={`text-xl font-bold ${
                    theme === "light" ? "text-blue-300" : "text-yellow-300"
                  }`}
                >
                  €{grandTotal}
                </span>
              </div>
            </div>
          </div>

          {/* Payment Form */}
          <div
            className={`rounded-2xl p-6 ${
              theme === "light"
                ? "bg-white shadow-lg"
                : "bg-[#13273F] shadow-lg shadow-blue-900/20 border border-cyan-500/10"
            }`}
          >
            <div className="flex items-center gap-3 mb-5">
              <div
                className={`p-2 rounded-full ${
                  theme === "light"
                    ? "bg-blue-100 text-blue-600"
                    : "bg-cyan-500/20 text-cyan-400"
                }`}
              >
                <CreditCard className="w-5 h-5" />
              </div>
              <h2
                className={`text-xl font-bold ${
                  theme === "light" ? "text-gray-800" : "text-white"
                }`}
              >
                Detalii Plată
              </h2>
            </div>
            <div className="space-y-4">
              <div>
                <label
                  className={`text-xs font-medium ${
                    theme === "light" ? "text-gray-600" : "text-gray-300"
                  }`}
                >
                  Nume pe card
                </label>
                <input
                  value={cardName}
                  onChange={(e) => setCardName(e.target.value)}
                  className={`mt-1 w-full rounded-lg px-3 py-2 text-sm outline-none border ${
                    theme === "light"
                      ? "bg-white border-blue-200 focus:border-blue-500"
                      : "bg-[#1E293B] border-cyan-800 focus:border-cyan-400 text-white"
                  }`}
                  placeholder="Ex: Andrei Pop"
                />
              </div>
              <div>
                <label
                  className={`text-xs font-medium ${
                    theme === "light" ? "text-gray-600" : "text-gray-300"
                  }`}
                >
                  Număr card
                </label>
                <input
                  value={cardNumber}
                  onChange={(e) => setCardNumber(e.target.value)}
                  className={`mt-1 w-full rounded-lg px-3 py-2 text-sm outline-none border tracking-wider ${
                    theme === "light"
                      ? "bg-white border-blue-200 focus:border-blue-500"
                      : "bg-[#1E293B] border-cyan-800 focus:border-cyan-400 text-white"
                  }`}
                  placeholder="4111 1111 1111 1111"
                />
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label
                    className={`text-xs font-medium ${
                      theme === "light" ? "text-gray-600" : "text-gray-300"
                    }`}
                  >
                    Expirare
                  </label>
                  <input
                    value={expiry}
                    onChange={(e) => setExpiry(e.target.value)}
                    className={`mt-1 w-full rounded-lg px-3 py-2 text-sm outline-none border ${
                      theme === "light"
                        ? "bg-white border-blue-200 focus:border-blue-500"
                        : "bg-[#1E293B] border-cyan-800 focus:border-cyan-400 text-white"
                    }`}
                    placeholder="MM/YY"
                  />
                </div>
                <div>
                  <label
                    className={`text-xs font-medium ${
                      theme === "light" ? "text-gray-600" : "text-gray-300"
                    }`}
                  >
                    CVV
                  </label>
                  <input
                    value={cvv}
                    onChange={(e) => setCvv(e.target.value)}
                    className={`mt-1 w-full rounded-lg px-3 py-2 text-sm outline-none border ${
                      theme === "light"
                        ? "bg-white border-blue-200 focus:border-blue-500"
                        : "bg-[#1E293B] border-cyan-800 focus:border-cyan-400 text-white"
                    }`}
                    placeholder="123"
                  />
                </div>
                <div>
                  <label
                    className={`text-xs font-medium ${
                      theme === "light" ? "text-gray-600" : "text-gray-300"
                    }`}
                  >
                    Email
                  </label>
                  <input
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className={`mt-1 w-full rounded-lg px-3 py-2 text-sm outline-none border ${
                      theme === "light"
                        ? "bg-white border-blue-200 focus:border-blue-500"
                        : "bg-[#1E293B] border-cyan-800 focus:border-cyan-400 text-white"
                    }`}
                    placeholder="email@exemplu.com"
                  />
                </div>
              </div>
              <label className="flex items-center gap-2 text-xs cursor-pointer select-none">
                <input
                  type="checkbox"
                  checked={acceptTerms}
                  onChange={(e) => setAcceptTerms(e.target.checked)}
                />
                <span
                  className={
                    theme === "light" ? "text-gray-600" : "text-gray-300"
                  }
                >
                  Accept termenii și condițiile și politica GDPR.
                </span>
              </label>
              <div className="flex items-center gap-2 text-[11px] mt-1">
                <ShieldCheck
                  className={`w-4 h-4 ${
                    theme === "light" ? "text-blue-500" : "text-cyan-400"
                  }`}
                />
                <span
                  className={
                    theme === "light" ? "text-gray-500" : "text-gray-400"
                  }
                >
                  Plata securizată prin gateway criptat.
                </span>
              </div>
              <button
                disabled={!formValid || processing}
                onClick={handlePay}
                className={`w-full rounded-xl py-3 text-sm font-semibold flex items-center justify-center gap-2 transition ${
                  formValid && !processing
                    ? theme === "light"
                      ? "bg-gradient-to-r from-blue-600 to-cyan-500 hover:shadow-lg hover:shadow-blue-400/30"
                      : "bg-gradient-to-r from-cyan-600 to-blue-600 hover:shadow-lg hover:shadow-cyan-600/40"
                    : "bg-gray-400/40 dark:bg-[#1E293B] cursor-not-allowed"
                } text-white`}
              >
                {processing ? "Procesare..." : "Plătește acum"}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div
        className={`fixed bottom-0 left-0 right-0 p-6 backdrop-blur-md ${
          theme === "light"
            ? "bg-white/90 border-t border-gray-200 shadow-lg"
            : "bg-[#0F233C]/90 border-t border-cyan-500/20 shadow-2xl shadow-blue-900/30"
        }`}
      >
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <p
              className={`text-sm mb-1 ${
                theme === "light" ? "text-gray-600" : "text-gray-400"
              }`}
            >
              Total de plată
            </p>
            <p
              className={`text-3xl font-bold ${
                theme === "light"
                  ? "bg-yellow-400 bg-clip-text text-transparent"
                  : "bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent"
              }`}
            >
              €{grandTotal}
            </p>
          </div>
          <button
            disabled={!formValid || processing}
            onClick={handlePay}
            className={`px-8 py-4 rounded-2xl font-bold text-white text-lg transition-all duration-300 ${
              formValid && !processing
                ? theme === "light"
                  ? "bg-gradient-to-r from-purple-600 to-blue-600 hover:shadow-xl hover:shadow-purple-500/30 hover:scale-105"
                  : "bg-gradient-to-r from-blue-600 to-cyan-600 hover:shadow-xl hover:shadow-cyan-500/50 hover:scale-105"
                : "bg-gray-400/40 dark:bg-[#1E293B] cursor-not-allowed"
            }`}
          >
            {processing ? "Procesare..." : "Plătește"}
          </button>
        </div>
      </div>
    </div>
  );
}
