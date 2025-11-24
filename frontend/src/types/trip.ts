export interface Flight {
  airline: string;
  price: number;
  isTopChoice?: boolean;
  originCode?: string;
  destinationCode?: string;
  departureTime?: string; // ISO or HH:MM
  arrivalTime?: string;
  duration?: string; // e.g. "3h 45m"
  stops?: string; // e.g. "Direct" or "1 stop in AMS"
  baggage?: string; // e.g. "Cabin bag + 23kg"
  cabinClass?: string; // e.g. "Economy", "Business"
}

export interface Accommodation {
  name: string;
  pricePerNight: number;
  distanceFromCenter: string;
  type: string;
  rating: number;
  isTopChoice?: boolean;
  image?: string;
  amenities?: string[]; // e.g. ["Wi-Fi","Pool","Gym"]
}

export interface ItineraryDay {
  day: number;
  title: string;
  description: string;
}

export interface TripPlan {
  destination: string;
  period: string;
  totalPrice: number;
  summary: string;
  flights: Flight[];
  accommodations: Accommodation[];
  itinerary: ItineraryDay[];
}
