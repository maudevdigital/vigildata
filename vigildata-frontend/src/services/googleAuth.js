// HU-10 - Login con Google via Supabase Auth.
// Usa supabase.auth.signInWithOAuth({provider:'google'}) y devuelve el
// access_token JWT de Supabase para enviarlo al backend (POST /auth/google).

import { createClient } from '@supabase/supabase-js'

let _supabase = null

export function getSupabase() {
  if (_supabase) return _supabase
  const url = import.meta.env.VITE_SUPABASE_URL
  const key = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY
  if (!url || !key) {
    throw new Error('Falta VITE_SUPABASE_URL / VITE_SUPABASE_PUBLISHABLE_KEY en .env')
  }
  _supabase = createClient(url, key, {
    auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true },
  })
  return _supabase
}

export async function obtenerIdTokenGoogle() {
  const supabase = getSupabase()
  // Si ya hay sesion activa devolvemos el access_token sin re-abrir popup.
  const { data: existing } = await supabase.auth.getSession()
  if (existing?.session?.access_token) return existing.session.access_token

  await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: { 
      redirectTo: window.location.origin + '/login',
      queryParams: {
        prompt: 'select_account'
      }
    },
  })
  // signInWithOAuth en modo redirect navega; el codigo siguiente solo aplica
  // si volvio del callback. Esperamos a que detectSessionInUrl complete.
  for (let i = 0; i < 50; i++) {
    const { data } = await supabase.auth.getSession()
    if (data?.session?.access_token) return data.session.access_token
    await new Promise((r) => setTimeout(r, 100))
  }
  throw new Error('No se obtuvo sesion de Supabase tras el login')
}

export async function cerrarSesionSupabase() {
  try {
    await getSupabase().auth.signOut()
  } catch {
    /* ignorar */
  }
}
