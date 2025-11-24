import { TripPlan } from "../types/trip";

export const mockTripPlan: TripPlan = {
  destination: "Shanghai",
  period: "4–18 December",
  totalPrice: 1450,
  summary:
    "Experience the perfect blend of ancient tradition and futuristic innovation in Shanghai. This curated 14-day journey takes you through iconic landmarks, hidden gems, and authentic local experiences. From the stunning Bund skyline to centuries-old temples, every day brings new discoveries in this vibrant metropolis.",
  flights: [
    {
      airline: "Qatar Airways",
      price: 720,
      isTopChoice: true,
      originCode: "OTP",
      destinationCode: "PVG",
      departureTime: "08:35",
      arrivalTime: "06:10",
      duration: "16h 35m",
      stops: "1 stop in DOH",
      baggage: "Cabin + 25kg",
      cabinClass: "Economy",
    },
    {
      airline: "KLM",
      price: 760,
      originCode: "OTP",
      destinationCode: "PVG",
      departureTime: "11:10",
      arrivalTime: "09:55",
      duration: "18h 45m",
      stops: "2 stops (AMS, CAN)",
      baggage: "Cabin + 23kg",
      cabinClass: "Economy",
    },
    {
      airline: "Turkish Airlines",
      price: 815,
      originCode: "OTP",
      destinationCode: "PVG",
      departureTime: "06:20",
      arrivalTime: "04:40",
      duration: "17h 20m",
      stops: "1 stop in IST",
      baggage: "Cabin + 30kg",
      cabinClass: "Economy",
    },
  ],
  accommodations: [
    {
      name: "The Riverside Luxury Suites",
      pricePerNight: 85,
      distanceFromCenter: "0.8 km from center",
      type: "2-bedroom apartment, private shower",
      rating: 9.2,
      isTopChoice: true,
      image:
        "https://images.pexels.com/photos/271639/pexels-photo-271639.jpeg?auto=compress&cs=tinysrgb&w=600",
      amenities: [
        "Wi-Fi",
        "Air Conditioning",
        "Gym",
        "Breakfast",
        "River View",
      ],
    },
    {
      name: "Jade Garden Hotel",
      pricePerNight: 72,
      distanceFromCenter: "1.2 km from center",
      type: "Deluxe room, city view",
      rating: 8.8,
      image:
        "https://images.pexels.com/photos/164595/pexels-photo-164595.jpeg?auto=compress&cs=tinysrgb&w=600",
      amenities: ["Wi-Fi", "Breakfast", "24h Reception", "Laundry"],
    },
    {
      name: "Modern Downtown Loft",
      pricePerNight: 95,
      distanceFromCenter: "0.5 km from center",
      type: "Studio apartment, skyline view",
      rating: 9.0,
      image:
        "https://images.pexels.com/photos/271805/pexels-photo-271805.jpeg?auto=compress&cs=tinysrgb&w=600",
      amenities: ["Wi-Fi", "Kitchenette", "Air Conditioning", "Workspace"],
    },
  ],
  itinerary: [
    {
      day: 1,
      title: "Bund River Walk & Arrival",
      description:
        "Arrive in Shanghai and settle into your accommodation. Evening stroll along the iconic Bund waterfront, featuring stunning colonial architecture and breathtaking skyline views across the Huangpu River.",
    },
    {
      day: 2,
      title: "Shanghai Tower & Observation Deck",
      description:
        "Visit the tallest building in China. Experience the world's highest observation deck at 546 meters, offering panoramic views of the entire city. Explore the modern Lujiazui financial district.",
    },
    {
      day: 3,
      title: "Jade Buddha Temple & Old City",
      description:
        "Discover the spiritual heart of Shanghai at this Buddhist temple featuring two precious jade statues. Wander through the atmospheric Old City and visit the historic Yuyuan Garden.",
    },
    {
      day: 4,
      title: "French Concession District",
      description:
        "Explore tree-lined streets, boutique shops, and charming cafes in this historic neighborhood. Visit Tianzifang, a maze of narrow alleyways filled with art studios and local crafts.",
    },
    {
      day: 5,
      title: "Shanghai Museum & People's Square",
      description:
        "Immerse yourself in Chinese art and history at one of the country's finest museums. Free admission with world-class collections of ceramics, bronze, and ancient jade.",
    },
    {
      day: 6,
      title: "Zhujiajiao Water Town Day Trip",
      description:
        "Escape the city to this Venice of the East. Cruise along ancient canals, walk over stone bridges dating back 400 years, and explore traditional Ming and Qing dynasty architecture.",
    },
    {
      day: 7,
      title: "Nanjing Road Shopping & Culture",
      description:
        "Experience China's premier shopping street. Browse international brands and local boutiques, then enjoy street food and people-watching in this bustling pedestrian paradise.",
    },
    {
      day: 8,
      title: "Xintiandi & Shikumen Architecture",
      description:
        "Discover beautifully preserved traditional Shikumen houses transformed into upscale restaurants and galleries. Learn about Shanghai's unique architectural heritage.",
    },
    {
      day: 9,
      title: "Shanghai Disneyland",
      description:
        "Full day at China's magical theme park featuring unique attractions like the TRON Lightcycle coaster and spectacular Castle of Magical Dreams shows.",
    },
    {
      day: 10,
      title: "Jing'an Temple & Contemporary Art",
      description:
        "Visit this golden Buddhist temple in the heart of the city. Afternoon at M50 Creative Park, Shanghai's cutting-edge contemporary art district.",
    },
    {
      day: 11,
      title: "Suzhou Day Trip",
      description:
        "High-speed train to nearby Suzhou, famous for its classical Chinese gardens. Visit the UNESCO-listed Humble Administrator's Garden and explore ancient canal streets.",
    },
    {
      day: 12,
      title: "Local Markets & Food Tour",
      description:
        "Dive into authentic Shanghai cuisine with a guided food tour. Visit local wet markets, taste xiaolongbao dumplings, and learn to make traditional dishes.",
    },
    {
      day: 13,
      title: "Oriental Pearl Tower & Riverside Cruise",
      description:
        "Ascend the iconic space-age tower for incredible views. Evening Huangpu River cruise with dinner, watching the city lights illuminate both ancient and modern architecture.",
    },
    {
      day: 14,
      title: "Departure & Last Moments",
      description:
        "Final morning to revisit favorite spots or last-minute shopping. Reflect on your incredible Shanghai adventure before heading to the airport.",
    },
  ],
};
