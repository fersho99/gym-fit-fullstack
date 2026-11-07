import { getMeApi } from "../api/user";

export function useUser() {
  const getMe = (token) => getMeApi(token);

  return { getMe };
}
