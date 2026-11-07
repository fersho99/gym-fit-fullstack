import React from "react";
import { Link } from "react-router-dom";

export function Error404() {
  return (
    <main className="error404">
      <h1>Página no encontrada</h1>
      <Link to="/">Volver al inicio</Link>
    </main>
  );
}
