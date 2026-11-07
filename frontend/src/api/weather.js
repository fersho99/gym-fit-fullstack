const WEATHER_URL = "https://api.open-meteo.com/v1/forecast";

export const CITY = {
  name: "Ciudad de México",
  latitude: 19.43,
  longitude: -99.13,
};

const DESCRIPTIONS = [
  [[0], "Despejado"],
  [[1, 2], "Parcialmente nublado"],
  [[3], "Nublado"],
  [[45, 48], "Niebla"],
  [[51, 53, 55, 56, 57], "Llovizna"],
  [[61, 63, 65, 66, 67, 80, 81, 82], "Lluvia"],
  [[71, 73, 75, 77, 85, 86], "Nieve"],
  [[95, 96, 99], "Tormenta"],
];

function describe(code) {
  const match = DESCRIPTIONS.find(([codes]) => codes.includes(code));
  return match ? match[1] : "Sin descripción";
}

export async function getWeatherApi(signal) {
  const query = new URLSearchParams({
    latitude: CITY.latitude,
    longitude: CITY.longitude,
    current:
      "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code",
    timezone: "auto",
  });

  const response = await fetch(`${WEATHER_URL}?${query}`, { signal });

  if (!response.ok) {
    throw new Error("No se pudo obtener el clima");
  }

  const { current } = await response.json();

  return {
    temperature: current.temperature_2m,
    feelsLike: current.apparent_temperature,
    humidity: current.relative_humidity_2m,
    wind: current.wind_speed_10m,
    description: describe(current.weather_code),
  };
}
