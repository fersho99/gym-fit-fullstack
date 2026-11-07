import React, { useEffect, useState } from "react";
import { Loader, Message } from "semantic-ui-react";
import { CITY, getWeatherApi } from "../api/weather";

export function WeatherWidget() {
  const [weather, setWeather] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    const controller = new AbortController();

    getWeatherApi(controller.signal)
      .then(setWeather)
      .catch((err) => {
        if (err.name !== "AbortError") setError(true);
      });

    return () => controller.abort();
  }, []);

  return (
    <section className="panel weather">
      <h2>Clima para entrenar en {CITY.name}</h2>

      {error && <Message negative content="No se pudo cargar el clima." />}
      {!error && !weather && <Loader active inline content="Cargando clima" />}
      {weather && (
        <>
          <div className="weather__temp">{weather.temperature} °C</div>
          <p className="weather__desc">{weather.description}</p>
          <dl>
            <dt>Sensación</dt>
            <dd>{weather.feelsLike} °C</dd>
            <dt>Humedad</dt>
            <dd>{weather.humidity} %</dd>
            <dt>Viento</dt>
            <dd>{weather.wind} km/h</dd>
          </dl>
          <p className="weather__source">Datos de Open-Meteo.com</p>
        </>
      )}
    </section>
  );
}
