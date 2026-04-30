export type LeadPlan = "avulso-1h" | "pacote-6h" | "pacote-12h";

export interface CreateLeadRequest {
  coach: "Mosca";
  nome: string;
  whatsapp: string;
  elo: number;
  plano: LeadPlan;
  objetivo: string;
  data?: string;
}

export interface CreateLeadResponse {
  ok: true;
  id: number;
}

export interface ApiErrorResponse {
  ok: false;
  error: string;
}

export interface Lead {
  id: number;
  coach: string;
  nome: string;
  whatsapp: string;
  elo: number;
  plano: LeadPlan;
  horas_avulsas: number | null;
  objetivo: string;
  data_cliente: string | null;
  created_at: string;
}

export interface ListLeadsResponse {
  count: number;
  items: Lead[];
}

