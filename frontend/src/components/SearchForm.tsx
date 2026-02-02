import React, { useState } from 'react';
import styled from 'styled-components';
import { Search, Loader } from 'lucide-react';

const SearchContainer = styled.div`
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const Title = styled.h2`
  color: #333;
  margin-bottom: 20px;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const Form = styled.form`
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  align-items: flex-end;
`;

const FormGroup = styled.div`
  flex: 1;
  min-width: 200px;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 500;
  font-size: 0.9rem;
`;

const Input = styled.input`
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  &::placeholder {
    color: #999;
  }
`;

const Select = styled.select`
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const Button = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 150px;
  justify-content: center;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
  }
  
  &:active:not(:disabled) {
    transform: translateY(0);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const HelpText = styled.p`
  color: #666;
  font-size: 0.85rem;
  margin-top: 10px;
  line-height: 1.4;
`;

interface SearchFormProps {
  onSearch: (brand: string, maxItems: number, source: 'all' | 'fragrantica' | 'sephora' | 'fragrancex') => void;
  loading: boolean;
}

const SearchForm: React.FC<SearchFormProps> = ({ onSearch, loading }) => {
  const [brand, setBrand] = useState('');
  const [maxItems, setMaxItems] = useState(25);
  const [source, setSource] = useState<'all' | 'fragrantica' | 'sephora' | 'fragrancex'>('all');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (brand.trim()) {
      onSearch(brand.trim(), maxItems, source);
    }
  };

  const popularBrands = [
    'Chanel', 'Dior', 'Tom Ford', 'Gucci', 'YSL',
    'Versace', 'Armani', 'Hugo Boss', 'Calvin Klein', 'Ralph Lauren',
    'Creed', 'Jo Malone', 'Byredo', 'Le Labo', 'Maison Francis Kurkdjian'
  ];

  return (
    <SearchContainer>
      <Title>
        <Search size={24} />
        Search Designer Perfumes
      </Title>
      
      <Form onSubmit={handleSubmit}>
        <FormGroup>
          <Label htmlFor="brand">Brand Name</Label>
          <Input
            id="brand"
            type="text"
            value={brand}
            onChange={(e) => setBrand(e.target.value)}
            placeholder="Enter designer brand (e.g., Chanel, Dior)"
            required
          />
        </FormGroup>
        
        <FormGroup>
          <Label htmlFor="maxItems">Max Items</Label>
          <Select
            id="maxItems"
            value={maxItems}
            onChange={(e) => setMaxItems(Number(e.target.value))}
          >
            <option value={10}>10 items</option>
            <option value={25}>25 items</option>
            <option value={50}>50 items</option>
            <option value={100}>100 items</option>
          </Select>
        </FormGroup>
        
        <FormGroup>
          <Label htmlFor="source">Data Source</Label>
          <Select
            id="source"
            value={source}
            onChange={(e) => setSource(e.target.value as any)}
          >
            <option value="all">All Sources</option>
            <option value="fragrantica">Fragrantica (Details + Reviews)</option>
            <option value="sephora">Sephora (Prices)</option>
            <option value="fragrancex">FragranceX (Prices)</option>
          </Select>
        </FormGroup>
        
        <Button type="submit" disabled={loading || !brand.trim()}>
          {loading ? (
            <>
              <Loader size={18} style={{ animation: 'spin 1s linear infinite' }} />
              Scraping...
            </>
          ) : (
            <>
              <Search size={18} />
              Search
            </>
          )}
        </Button>
      </Form>
      
      <HelpText>
        <strong>Popular brands:</strong> {popularBrands.join(', ')}
        <br />
        <strong>Fragrantica:</strong> Best for detailed fragrance notes, ratings, and reviews
        <br />
        <strong>Sephora/FragranceX:</strong> Best for pricing and availability information
      </HelpText>
    </SearchContainer>
  );
};

export default SearchForm;