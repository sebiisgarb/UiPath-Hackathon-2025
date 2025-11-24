import { useState } from "react";
import { useTheme } from "./context/ThemeContext";
import { Header } from "./components/Header";
import { InputCard } from "./components/InputCard";
import { CloudAnimation } from "./components/CloudAnimation";
import { StarAnimation } from "./components/StarAnimation";
// Recommendation components removed in favor of unified PlanSummary
import { CheckoutPage } from "./pages/CheckoutPage";
import { PaymentPage } from "./pages/PaymentPage";
import { mockTripPlan } from "./data/mockData";

// NEW COMPONENTS
import { HomeHero } from "./components/HomeHero";
import { AboutUs } from "./components/AboutUs";
import PlanSummary from "./components/PlanSummary.tsx";
import { Flight, Accommodation } from "./types/trip";

type Page = "home" | "checkout" | "payment";

function App() {
  const { theme } = useTheme();
  const [hasGenerated, setHasGenerated] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState<Page>("home");
  const [showChat, setShowChat] = useState(false);
  const [selectedFlight, setSelectedFlight] = useState<Flight | null>(null);
  const [selectedHotel, setSelectedHotel] = useState<Accommodation | null>(
    null
  );
  const [destination, setDestination] = useState("");
  const [travelDates, setTravelDates] = useState("");
  const [backendFlights, setBackendFlights] = useState<Flight[]>([]);
  const [backendHotels, setBackendHotels] = useState<Accommodation[]>([]);
  const [backendItinerary, setBackendItinerary] = useState<any[]>([]);
  const [tripComplete, setTripComplete] = useState(false);

  const handleGenerate = () => {
    setIsLoading(true);
    setTimeout(() => {
      setHasGenerated(true);
      setIsLoading(false);
    }, 1500);
  };

  const handleNewPlan = () => {
    setHasGenerated(false);
    setIsLoading(false);
    setCurrentPage("home");
    setShowChat(false);
    setSelectedFlight(null);
    setSelectedHotel(null);
    setDestination("");
    setTravelDates("");
  };

  // Chat heuristics capture destination & dates directly
  const handleCaptureDestination = (value: string) => setDestination(value);
  const handleCaptureDates = (value: string) => setTravelDates(value);
  const handleBackendComplete = () => handleGenerate();

  // Handle backend data updates
  const handleBackendData = (data?: {
    flights?: any[];
    hotels?: any[];
    itinerary?: any[];
  }) => {
    if (data?.flights && data.flights.length > 0) {
      setBackendFlights(data.flights);
      // Auto-select first flight if available
      if (!selectedFlight) {
        setSelectedFlight(data.flights[0]);
      }
    }
    if (data?.hotels && data.hotels.length > 0) {
      setBackendHotels(data.hotels);
      // Auto-select first hotel if available
      if (!selectedHotel) {
        setSelectedHotel(data.hotels[0]);
      }
    }
    if (data?.itinerary) {
      setBackendItinerary(data.itinerary);
    }

    // Check if all required fields are complete
    const hasDestination = destination && destination.length > 0;
    const hasDates = travelDates && travelDates.length > 0;
    const hasFlight =
      selectedFlight !== null || (data?.flights && data.flights.length > 0);
    const hasHotel =
      selectedHotel !== null || (data?.hotels && data.hotels.length > 0);
    const hasItinerary =
      backendItinerary.length > 0 ||
      (data?.itinerary && data.itinerary.length > 0);

    // 🔍 DEBUG: Progres către PlanSummary
    console.log("📊 PROGRES CĂTRE PLANSUMMARY:", {
      "✅ Destinație": hasDestination ? destination : "❌ LIPSEȘTE",
      "✅ Date": hasDates ? travelDates : "❌ LIPSEȘTE",
      "✅ Zbor": hasFlight
        ? selectedFlight
          ? `${selectedFlight.airline} - ${selectedFlight.price}€`
          : "Detectat din backend"
        : "❌ LIPSEȘTE",
      "✅ Hotel": hasHotel
        ? selectedHotel
          ? `${selectedHotel.name} - ${selectedHotel.pricePerNight}€/noapte`
          : "Detectat din backend"
        : "❌ LIPSEȘTE",
      "✅ Itinerariu": hasItinerary
        ? `${data?.itinerary?.length || backendItinerary.length} activități`
        : "❌ LIPSEȘTE",
      "🎯 TRIP COMPLETE":
        hasDestination && hasDates && hasFlight && hasHotel && hasItinerary
          ? "✅ DA! Pagina se va afișa!"
          : "❌ NU - mai completează câmpurile de mai sus",
    });

    if (hasDestination && hasDates && hasFlight && hasHotel && hasItinerary) {
      console.log("🎉 BRAVO! Se afișează PlanSummary!");
      setTripComplete(true);
      setHasGenerated(true);
    }
  };

  const nights = (() => {
    const match = travelDates.match(/(\d{1,2})\s*[-–]\s*(\d{1,2})/);
    if (!match) return 3;
    const start = parseInt(match[1]);
    const end = parseInt(match[2]);
    const diff = end - start;
    return diff > 0 && diff < 60 ? diff : 3;
  })();

  const handleBuyNow = () => setCurrentPage("checkout");
  const handleBackToHome = () => setCurrentPage("home");
  const handleProceedToPayment = () => setCurrentPage("payment");

  // CHECKOUT PAGE
  if (currentPage === "checkout") {
    return (
      <div
        className={`min-h-screen transition-all duration-500 ${
          theme === "light"
            ? "bg-[#d7efff]"
            : "bg-gradient-to-br from-[#0A1A2F] via-[#0F233C] to-[#0A1A2F]"
        }`}
      >
        {theme === "light" ? <CloudAnimation /> : <StarAnimation />}
        <Header onNewPlan={handleNewPlan} />
        <CheckoutPage
          flight={selectedFlight}
          hotel={selectedHotel}
          nights={nights}
          destination={destination || mockTripPlan.destination}
          travelDates={travelDates || mockTripPlan.period}
          onBack={handleBackToHome}
          onProceedToPayment={handleProceedToPayment}
        />
      </div>
    );
  }

  // PAYMENT PAGE
  if (currentPage === "payment") {
    return (
      <div
        className={`min-h-screen transition-all duration-500 ${
          theme === "light"
            ? "bg-[#d7efff]"
            : "bg-gradient-to-br from-[#0A1A2F] via-[#0F233C] to-[#0A1A2F]"
        }`}
      >
        {theme === "light" ? <CloudAnimation /> : <StarAnimation />}
        <Header onNewPlan={handleNewPlan} />
        <PaymentPage onBack={handleBackToHome} />
      </div>
    );
  }

  // HOME PAGE
  return (
    <div
      className={`min-h-screen transition-all duration-500 ${
        theme === "light"
          ? "bg-gradient-to-br from-[#d7efff] to-[#d7efff]"
          : "bg-gradient-to-br from-[#0A1A2F] to-[#0A1A2F]"
      }`}
    >
      {theme === "light" ? <CloudAnimation /> : <StarAnimation />}

      <Header
        onNewPlan={handleNewPlan}
        showStepper={false}
        hasGenerated={hasGenerated}
      />

      {/* 🔹 Homepage BEFORE starting the planner */}
      {!showChat && !hasGenerated && (
        <>
          <div className="relative z-10">
            <HomeHero onStart={() => setShowChat(true)} />
          </div>

          <div className="relative z-10 mt-">
            <AboutUs />
          </div>
        </>
      )}

      {/* 🔹 AI Planner ONLY (no results yet) */}
      {showChat && !tripComplete && (
        <div className="relative z-10 pt-28 pb-16">
          <div className="max-w-3xl mx-auto px-6 flex justify-center">
            <InputCard
              isMinimized={false}
              isLoading={isLoading && !hasGenerated}
              onCaptureDestination={handleCaptureDestination}
              onCaptureDates={handleCaptureDates}
              onBackendComplete={handleBackendComplete}
              onBackendData={handleBackendData}
              flights={backendFlights}
              hotels={backendHotels}
              onSelectFlight={setSelectedFlight}
              onSelectHotel={setSelectedHotel}
            />
          </div>
        </div>
      )}

      {/* 🔹 SPLIT VIEW: Chat (1/3 right) + PlanSummary (2/3 left) */}
      {tripComplete && (
        <div className="relative z-10 pt-20 pb-20">
          <div className="max-w-[95%] mx-auto px-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">
              {/* LEFT SIDE - 2/3 - PlanSummary */}
              <div className="lg:col-span-2 overflow-y-auto">
                <div className="mb-6">
                  <h1
                    className={`text-3xl font-bold mb-2 ${
                      theme === "light" ? "text-[#3f6794]" : "text-white"
                    }`}
                  >
                    🎉 Planul Tău de Călătorie
                  </h1>
                  <p
                    className={`text-sm ${
                      theme === "light" ? "text-gray-600" : "text-gray-300"
                    }`}
                  >
                    Toate detaliile călătoriei tale au fost finalizate.
                  </p>
                </div>
                <PlanSummary
                  destination={destination || mockTripPlan.destination}
                  travelDates={travelDates || mockTripPlan.period}
                  flight={selectedFlight}
                  hotel={selectedHotel}
                  nights={nights}
                  onBookNow={handleBuyNow}
                />
              </div>

              {/* RIGHT SIDE - 1/3 - Chat (minimized/sticky) */}
              <div className="lg:col-span-1">
                <div className="sticky top-24">
                  <InputCard
                    isMinimized={true}
                    isLoading={false}
                    onCaptureDestination={handleCaptureDestination}
                    onCaptureDates={handleCaptureDates}
                    onBackendComplete={handleBackendComplete}
                    onBackendData={handleBackendData}
                    flights={backendFlights}
                    hotels={backendHotels}
                    onSelectFlight={setSelectedFlight}
                    onSelectHotel={setSelectedHotel}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
