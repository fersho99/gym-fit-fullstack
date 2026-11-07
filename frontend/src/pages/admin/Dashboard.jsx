import React from "react";
import { Button } from "semantic-ui-react";
import { useAuth } from "../../hooks/useAuth";
import { WeatherWidget } from "../../components/WeatherWidget";

export function Dashboard() {
  const { logout, auth } = useAuth();
  const user = auth.me;
  const fullName = `${user.first_name} ${user.last_name}`.trim();

  return (
    <main className="dashboard">
      <header className="dashboard__header">
        <div>
          <h1>Hola, {fullName || user.username}</h1>
          <p>Panel de socio de Gym Fit</p>
        </div>
        <Button content="Cerrar sesión" onClick={logout} />
      </header>

      <div className="dashboard__grid">
        <section className="panel">
          <h2>Mis datos</h2>
          <dl>
            <dt>Usuario</dt>
            <dd>{user.username}</dd>
            <dt>Correo</dt>
            <dd>{user.email}</dd>
            <dt>Teléfono</dt>
            <dd>{user.telefono || "Sin registrar"}</dd>
          </dl>
        </section>

        <WeatherWidget />
      </div>
    </main>
  );
}
