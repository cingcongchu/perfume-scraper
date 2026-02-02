export interface Perfume {
  id: number;
  name: string;
  brand: string;
  designer: string;
  price: number | null;
  size: string | null;
  description: string | null;
  notes: string | null;
  image_url: string | null;
  source_url: string | null;
  // Fragrantica-specific fields
  rating: number | null;
  gender: string | null;
  year: number | null;
  top_notes: string | null;
  middle_notes: string | null;
  base_notes: string | null;
  longevity: string | null;
  sillage: string | null;
  created_at: string;
  updated_at: string;
}

export interface ScrapingRequest {
  brand: string;
  max_items?: number;
  source?: 'all' | 'fragrantica' | 'sephora' | 'fragrancex';
}