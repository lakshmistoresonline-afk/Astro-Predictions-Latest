export interface DistrictCityItem {
  district: string
  latitude: number
  longitude: number
  timezone_str: string
}

export interface StateItem {
  state_name: string
  districts: DistrictCityItem[]
}

export interface CountryItem {
  country_name: string
  states: StateItem[]
}

export const CASCADING_LOCATIONS: CountryItem[] = [
  {
    country_name: "India",
    states: [
      {
        state_name: "Kerala",
        districts: [
          { district: "Palakkad", latitude: 10.7867, longitude: 76.6548, timezone_str: "Asia/Kolkata" },
          { district: "Kochi (Ernakulam)", latitude: 9.9312, longitude: 76.2673, timezone_str: "Asia/Kolkata" },
          { district: "Thiruvananthapuram", latitude: 8.5241, longitude: 76.9366, timezone_str: "Asia/Kolkata" },
          { district: "Thrissur", latitude: 10.5276, longitude: 76.2144, timezone_str: "Asia/Kolkata" },
          { district: "Kozhikode", latitude: 11.2588, longitude: 75.7804, timezone_str: "Asia/Kolkata" },
          { district: "Kottayam", latitude: 9.5916, longitude: 76.5222, timezone_str: "Asia/Kolkata" },
          { district: "Kollam", latitude: 8.8932, longitude: 76.6141, timezone_str: "Asia/Kolkata" },
          { district: "Alappuzha", latitude: 9.4981, longitude: 76.3388, timezone_str: "Asia/Kolkata" },
          { district: "Kannur", latitude: 11.8745, longitude: 75.3704, timezone_str: "Asia/Kolkata" },
          { district: "Malappuram", latitude: 11.0722, longitude: 76.0740, timezone_str: "Asia/Kolkata" },
          { district: "Pathanamthitta", latitude: 9.2648, longitude: 76.7870, timezone_str: "Asia/Kolkata" },
          { district: "Idukki", latitude: 9.8494, longitude: 76.9810, timezone_str: "Asia/Kolkata" },
          { district: "Wayanad (Kalpetta)", latitude: 11.6103, longitude: 76.0827, timezone_str: "Asia/Kolkata" },
          { district: "Kasaragod", latitude: 12.5102, longitude: 74.9852, timezone_str: "Asia/Kolkata" }
        ]
      },
      {
        state_name: "Tamil Nadu",
        districts: [
          { district: "Chennai", latitude: 13.0827, longitude: 80.2707, timezone_str: "Asia/Kolkata" },
          { district: "Coimbatore", latitude: 11.0168, longitude: 76.9558, timezone_str: "Asia/Kolkata" },
          { district: "Madurai", latitude: 9.9252, longitude: 78.1198, timezone_str: "Asia/Kolkata" },
          { district: "Salem", latitude: 11.6643, longitude: 78.1460, timezone_str: "Asia/Kolkata" },
          { district: "Tiruchirappalli", latitude: 10.7905, longitude: 78.7047, timezone_str: "Asia/Kolkata" },
          { district: "Tirunelveli", latitude: 8.7139, longitude: 77.7567, timezone_str: "Asia/Kolkata" },
          { district: "Vellore", latitude: 12.9165, longitude: 79.1325, timezone_str: "Asia/Kolkata" },
          { district: "Erode", latitude: 11.3410, longitude: 77.7172, timezone_str: "Asia/Kolkata" },
          { district: "Thanjavur", latitude: 10.7870, longitude: 79.1378, timezone_str: "Asia/Kolkata" },
          { district: "Kanchipuram", latitude: 12.8342, longitude: 79.7036, timezone_str: "Asia/Kolkata" },
          { district: "Dindigul", latitude: 10.3673, longitude: 77.9803, timezone_str: "Asia/Kolkata" }
        ]
      },
      {
        state_name: "Karnataka",
        districts: [
          { district: "Bengaluru", latitude: 12.9716, longitude: 77.5946, timezone_str: "Asia/Kolkata" },
          { district: "Mysuru", latitude: 12.2958, longitude: 76.6394, timezone_str: "Asia/Kolkata" },
          { district: "Mangaluru", latitude: 12.9141, longitude: 74.8560, timezone_str: "Asia/Kolkata" },
          { district: "Hubballi-Dharwad", latitude: 15.3647, longitude: 75.1240, timezone_str: "Asia/Kolkata" },
          { district: "Belagavi", latitude: 15.8497, longitude: 74.4977, timezone_str: "Asia/Kolkata" },
          { district: "Shivamogga", latitude: 13.9299, longitude: 75.5681, timezone_str: "Asia/Kolkata" },
          { district: "Udupi", latitude: 13.3409, longitude: 74.7421, timezone_str: "Asia/Kolkata" },
          { district: "Tumakuru", latitude: 13.3392, longitude: 77.1022, timezone_str: "Asia/Kolkata" }
        ]
      },
      {
        state_name: "Maharashtra",
        districts: [
          { district: "Mumbai", latitude: 18.9220, longitude: 72.8347, timezone_str: "Asia/Kolkata" },
          { district: "Pune", latitude: 18.5204, longitude: 73.8567, timezone_str: "Asia/Kolkata" },
          { district: "Nagpur", latitude: 21.1458, longitude: 79.0882, timezone_str: "Asia/Kolkata" },
          { district: "Nashik", latitude: 19.9975, longitude: 73.7898, timezone_str: "Asia/Kolkata" },
          { district: "Thane", latitude: 19.2183, longitude: 72.9781, timezone_str: "Asia/Kolkata" },
          { district: "Chhatrapati Sambhajinagar (Aurangabad)", latitude: 19.8762, longitude: 75.3433, timezone_str: "Asia/Kolkata" },
          { district: "Solapur", latitude: 17.6599, longitude: 75.9064, timezone_str: "Asia/Kolkata" },
          { district: "Kolhapur", latitude: 16.7050, longitude: 74.2433, timezone_str: "Asia/Kolkata" }
        ]
      },
      {
        state_name: "Delhi",
        districts: [
          { district: "New Delhi", latitude: 28.6139, longitude: 77.2090, timezone_str: "Asia/Kolkata" },
          { district: "North Delhi", latitude: 28.7041, longitude: 77.1025, timezone_str: "Asia/Kolkata" },
          { district: "South Delhi", latitude: 28.5355, longitude: 77.2610, timezone_str: "Asia/Kolkata" }
        ]
      },
      {
        state_name: "Gujarat",
        districts: [
          { district: "Ahmedabad", latitude: 23.0225, longitude: 72.5714, timezone_str: "Asia/Kolkata" },
          { district: "Surat", latitude: 21.1702, longitude: 72.8311, timezone_str: "Asia/Kolkata" },
          { district: "Vadodara", latitude: 22.3072, longitude: 73.1812, timezone_str: "Asia/Kolkata" },
          { district: "Rajkot", latitude: 22.3039, longitude: 70.8022, timezone_str: "Asia/Kolkata" },
          { district: "Gandhinagar", latitude: 23.2156, longitude: 72.6369, timezone_str: "Asia/Kolkata" }
        ]
      },
      {
        state_name: "Uttar Pradesh",
        districts: [
          { district: "Lucknow", latitude: 26.8467, longitude: 80.9462, timezone_str: "Asia/Kolkata" },
          { district: "Varanasi", latitude: 25.3176, longitude: 82.9739, timezone_str: "Asia/Kolkata" },
          { district: "Kanpur", latitude: 26.4499, longitude: 80.3319, timezone_str: "Asia/Kolkata" },
          { district: "Agra", latitude: 27.1767, longitude: 78.0081, timezone_str: "Asia/Kolkata" },
          { district: "Prayagraj (Allahabad)", latitude: 25.4358, longitude: 81.8463, timezone_str: "Asia/Kolkata" },
          { district: "Noida / Greater Noida", latitude: 28.5355, longitude: 77.3910, timezone_str: "Asia/Kolkata" }
        ]
      },
      {
        state_name: "West Bengal",
        districts: [
          { district: "Kolkata", latitude: 22.5726, longitude: 88.3639, timezone_str: "Asia/Kolkata" },
          { district: "Siliguri", latitude: 26.7271, longitude: 88.3953, timezone_str: "Asia/Kolkata" },
          { district: "Howrah", latitude: 22.5958, longitude: 88.2636, timezone_str: "Asia/Kolkata" }
        ]
      },
      {
        state_name: "Telangana",
        districts: [
          { district: "Hyderabad", latitude: 17.3850, longitude: 78.4867, timezone_str: "Asia/Kolkata" },
          { district: "Warangal", latitude: 17.9689, longitude: 79.5941, timezone_str: "Asia/Kolkata" },
          { district: "Nizamabad", latitude: 18.6725, longitude: 78.0941, timezone_str: "Asia/Kolkata" }
        ]
      },
      {
        state_name: "Andhra Pradesh",
        districts: [
          { district: "Visakhapatnam", latitude: 17.6868, longitude: 83.2185, timezone_str: "Asia/Kolkata" },
          { district: "Vijayawada", latitude: 16.5062, longitude: 80.6480, timezone_str: "Asia/Kolkata" },
          { district: "Tirupati", latitude: 13.6288, longitude: 79.4192, timezone_str: "Asia/Kolkata" }
        ]
      },
      {
        state_name: "Punjab",
        districts: [
          { district: "Amritsar", latitude: 31.6340, longitude: 74.8723, timezone_str: "Asia/Kolkata" },
          { district: "Ludhiana", latitude: 30.9010, longitude: 75.8573, timezone_str: "Asia/Kolkata" },
          { district: "Jalandhar", latitude: 31.3260, longitude: 75.5762, timezone_str: "Asia/Kolkata" }
        ]
      },
      {
        state_name: "Rajasthan",
        districts: [
          { district: "Jaipur", latitude: 26.9124, longitude: 75.7873, timezone_str: "Asia/Kolkata" },
          { district: "Jodhpur", latitude: 26.2389, longitude: 73.0243, timezone_str: "Asia/Kolkata" },
          { district: "Udaipur", latitude: 24.5854, longitude: 73.7125, timezone_str: "Asia/Kolkata" }
        ]
      }
    ]
  },
  {
    country_name: "United Kingdom",
    states: [
      {
        state_name: "England",
        districts: [
          { district: "London", latitude: 51.5074, longitude: -0.1278, timezone_str: "Europe/London" },
          { district: "Manchester", latitude: 53.4808, longitude: -2.2426, timezone_str: "Europe/London" },
          { district: "Birmingham", latitude: 52.4862, longitude: -1.8904, timezone_str: "Europe/London" }
        ]
      },
      {
        state_name: "Scotland",
        districts: [
          { district: "Edinburgh", latitude: 55.9533, longitude: -3.1883, timezone_str: "Europe/London" },
          { district: "Glasgow", latitude: 55.8642, longitude: -4.2518, timezone_str: "Europe/London" }
        ]
      }
    ]
  },
  {
    country_name: "United States",
    states: [
      {
        state_name: "California",
        districts: [
          { district: "Los Angeles", latitude: 34.0522, longitude: -118.2437, timezone_str: "America/Los_Angeles" },
          { district: "San Francisco", latitude: 37.7749, longitude: -122.4194, timezone_str: "America/Los_Angeles" },
          { district: "San Jose / Silicon Valley", latitude: 37.3382, longitude: -121.8863, timezone_str: "America/Los_Angeles" }
        ]
      },
      {
        state_name: "New York",
        districts: [
          { district: "New York City", latitude: 40.7128, longitude: -74.0060, timezone_str: "America/New_York" },
          { district: "Buffalo", latitude: 42.8864, longitude: -78.8784, timezone_str: "America/New_York" }
        ]
      },
      {
        state_name: "Texas",
        districts: [
          { district: "Houston", latitude: 29.7604, longitude: -95.3698, timezone_str: "America/Chicago" },
          { district: "Dallas", latitude: 32.7767, longitude: -96.7970, timezone_str: "America/Chicago" },
          { district: "Austin", latitude: 30.2672, longitude: -97.7431, timezone_str: "America/Chicago" }
        ]
      }
    ]
  },
  {
    country_name: "United Arab Emirates",
    states: [
      {
        state_name: "Dubai Emirate",
        districts: [
          { district: "Dubai", latitude: 25.2048, longitude: 55.2708, timezone_str: "Asia/Dubai" }
        ]
      },
      {
        state_name: "Abu Dhabi Emirate",
        districts: [
          { district: "Abu Dhabi", latitude: 24.4539, longitude: 54.3773, timezone_str: "Asia/Dubai" }
        ]
      }
    ]
  },
  {
    country_name: "Singapore",
    states: [
      {
        state_name: "Singapore Central Region",
        districts: [
          { district: "Singapore City", latitude: 1.3521, longitude: 103.8198, timezone_str: "Asia/Singapore" }
        ]
      }
    ]
  }
]
