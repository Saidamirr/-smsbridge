import {apiFetch} from "@/lib/shared/api";
import type {Country, Order, Price, Service, UserLimit, Wallet} from "@/lib/shared/types";

export function getBalance() {
  return apiFetch<Wallet>("/api/v1/balance");
}

export function getLimits() {
  return apiFetch<UserLimit>("/api/v1/limits");
}

export function getServices() {
  return apiFetch<Service[]>("/api/v1/services");
}

export function getCountries() {
  return apiFetch<Country[]>("/api/v1/countries");
}

export function getPrices(serviceCode?: string, countryIso2?: string) {
  const query = new URLSearchParams();
  if (serviceCode) query.set("service_code", serviceCode);
  if (countryIso2) query.set("country_iso2", countryIso2);
  return apiFetch<Price[]>(`/api/v1/prices?${query}`);
}

export function listOrders(filters: {status?: string; service?: string; country?: string} = {}) {
  const query = new URLSearchParams();
  if (filters.status) query.set("status", filters.status);
  if (filters.service) query.set("service", filters.service);
  if (filters.country) query.set("country", filters.country);
  return apiFetch<Order[]>(`/api/v1/orders?${query}`);
}

export function getOrder(publicId: string) {
  return apiFetch<Order>(`/api/v1/orders/${publicId}`);
}

export function createOrder(payload: {service_code: string; country_iso2: string; operator?: string | null}) {
  return apiFetch<Order>("/api/v1/orders", {method: "POST", body: JSON.stringify(payload)});
}

export function cancelOrder(publicId: string) {
  return apiFetch<Order>(`/api/v1/orders/${publicId}/cancel`, {method: "POST"});
}

export function finishOrder(publicId: string) {
  return apiFetch<Order>(`/api/v1/orders/${publicId}/finish`, {method: "POST"});
}

export function regenerateApiKey() {
  return apiFetch<{api_key: string; message: string}>("/api/v1/api-key/regenerate", {method: "POST"});
}

