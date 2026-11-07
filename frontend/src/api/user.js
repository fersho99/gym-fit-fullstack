const API_URL = import.meta.env.VITE_BASE_API_URL;

// fetch solo falla si no hay conexión; los errores HTTP se revisan aparte.
async function request(path, params) {
  try {
    return await fetch(`${API_URL}${path}`, params);
  } catch {
    throw new Error("No se pudo conectar con el servidor");
  }
}

export async function loginApi(formData) {
  const response = await request("/api/v1/auth/token/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  });

  if (response.status !== 200) {
    throw new Error("Usuario o contraseña incorrecta");
  }

  return response.json();
}

export async function registerApi({ username, email, password }) {
  const response = await request("/api/v1/auth/register/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password }),
  });

  const result = await response.json();

  if (response.status !== 201) {
    // Django responde { campo: ["mensaje"] }; se muestra el primer mensaje.
    const [firstError] = Object.values(result).flat();
    throw new Error(firstError || "No se pudo crear el usuario");
  }

  return result;
}

export async function getMeApi(token) {
  const response = await request("/api/v1/auth/me/", {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (response.status !== 200) {
    throw new Error("La sesión no es válida");
  }

  return response.json();
}
