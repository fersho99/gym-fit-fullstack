import React from "react";
import { Link } from "react-router-dom";
import { Button } from "semantic-ui-react";

export function Home() {
  return (
    <main className="home">
      <h1>Gym Fit</h1>
      <p>Tu cuenta de socio, en un solo lugar.</p>
      <div>
        <Button as={Link} to="/login" primary content="Iniciar sesión" />
        <Button as={Link} to="/register" content="Crear cuenta" />
      </div>
    </main>
  );
}
