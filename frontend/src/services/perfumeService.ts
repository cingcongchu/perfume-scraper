import axios from 'axios';
import { Perfume, ScrapingRequest } from '../types/perfume';

// Dynamic API URL - uses environment variable or defaults to local
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://perfume-scraper-backend.onrender.com'  // Production backend URL
    : 'http://localhost:8002');  // Local development (sesuaikan dengan port backend)

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const perfumeService = {
  async getPerfumes(brand?: string, skip: number = 0, limit: number = 100): Promise<Perfume[]> {
    const params = new URLSearchParams();
    if (brand) params.append('brand', brand);
    params.append('skip', skip.toString());
    params.append('limit', limit.toString());
    
    const response = await api.get(`/api/perfumes?${params}`);
    return response.data;
  },

  async getPerfume(id: number): Promise<Perfume> {
    const response = await api.get(`/api/perfumes/${id}`);
    return response.data;
  },

  async scrapePerfumes(
    brand: string, 
    maxItems: number = 50, 
    source: 'all' | 'fragrantica' | 'sephora' | 'fragrancex' = 'all'
  ): Promise<Perfume[]> {
    const request: ScrapingRequest = { brand, max_items: maxItems, source };
    const response = await api.post('/api/perfumes/scrape', request);
    return response.data;
  },

  async deletePerfume(id: number): Promise<void> {
    await api.delete(`/api/perfumes/${id}`);
  },

  async getBrands(): Promise<string[]> {
    const response = await api.get('/api/perfumes/brands/list');
    return response.data.brands;
  }
};