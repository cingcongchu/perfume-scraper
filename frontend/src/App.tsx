import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { Search, Sparkles, Package, DollarSign } from 'lucide-react';
import PerfumeCard from './components/PerfumeCard';
import SearchForm from './components/SearchForm';
import { perfumeService } from './services/perfumeService';
import { Perfume } from './types/perfume';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
`;

const Header = styled.header`
  text-align: center;
  margin-bottom: 40px;
  color: white;
`;

const Title = styled.h1`
  font-size: 3rem;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 30px;
`;

const StatsContainer = styled.div`
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 30px;
  flex-wrap: wrap;
`;

const StatCard = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 15px 25px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const MainContent = styled.main`
  max-width: 1200px;
  margin: 0 auto;
`;

const LoadingSpinner = styled.div`
  text-align: center;
  padding: 40px;
  color: white;
  font-size: 1.2rem;
`;

const ErrorMessage = styled.div`
  background: rgba(255, 0, 0, 0.1);
  border: 1px solid rgba(255, 0, 0, 0.3);
  color: white;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 20px;
  text-align: center;
`;

const PerfumeGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
  margin-top: 30px;
`;

const EmptyState = styled.div`
  text-align: center;
  color: white;
  padding: 60px 20px;
  
  h3 {
    font-size: 1.5rem;
    margin-bottom: 15px;
    opacity: 0.9;
  }
  
  p {
    opacity: 0.7;
    font-size: 1.1rem;
  }
`;

const App: React.FC = () => {
  const [perfumes, setPerfumes] = useState<Perfume[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState({
    total: 0,
    brands: 0,
    avgPrice: 0
  });

  useEffect(() => {
    loadPerfumes();
  }, []);

  const loadPerfumes = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await perfumeService.getPerfumes();
      setPerfumes(data);
      updateStats(data);
    } catch (err) {
      setError('Failed to load perfumes. Please try again.');
      console.error('Error loading perfumes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (
    brand: string, 
    maxItems: number, 
    source: 'all' | 'fragrantica' | 'sephora' | 'fragrancex'
  ) => {
    try {
      setLoading(true);
      setError(null);
      const data = await perfumeService.scrapePerfumes(brand, maxItems, source);
      setPerfumes(prev => [...prev, ...data]);
      updateStats([...perfumes, ...data]);
    } catch (err) {
      setError(`Failed to scrape ${brand}. Please try again.`);
      console.error('Error scraping perfumes:', err);
    } finally {
      setLoading(false);
    }
  };

  const updateStats = (perfumeList: Perfume[]) => {
    const uniqueBrands = new Set(perfumeList.map(p => p.brand)).size;
    const validPrices = perfumeList.filter(p => p.price !== null).map(p => p.price!);
    const avgPrice = validPrices.length > 0 
      ? validPrices.reduce((sum, price) => sum + price, 0) / validPrices.length 
      : 0;

    setStats({
      total: perfumeList.length,
      brands: uniqueBrands,
      avgPrice: avgPrice
    });
  };

  const handleDelete = async (id: number) => {
    try {
      await perfumeService.deletePerfume(id);
      setPerfumes(prev => prev.filter(p => p.id !== id));
      updateStats(perfumes.filter(p => p.id !== id));
    } catch (err) {
      setError('Failed to delete perfume. Please try again.');
      console.error('Error deleting perfume:', err);
    }
  };

  return (
    <AppContainer>
      <Header>
        <Title>
          <Sparkles size={40} />
          Perfume Scraper
        </Title>
        <Subtitle>
          Discover and collect perfumes from Fragrantica, Sephora, and FragranceX
        </Subtitle>
        
        <StatsContainer>
          <StatCard>
            <Package size={20} />
            <span>{stats.total} Perfumes</span>
          </StatCard>
          <StatCard>
            <Search size={20} />
            <span>{stats.brands} Brands</span>
          </StatCard>
          <StatCard>
            <DollarSign size={20} />
            <span>${stats.avgPrice.toFixed(2)} Avg Price</span>
          </StatCard>
        </StatsContainer>
      </Header>

      <MainContent>
        <SearchForm onSearch={handleSearch} loading={loading} />
        
        {error && <ErrorMessage>{error}</ErrorMessage>}
        
        {loading && (
          <LoadingSpinner>
            <Sparkles size={30} style={{ animation: 'spin 1s linear infinite' }} />
            <p>Scraping perfumes... This may take a moment.</p>
          </LoadingSpinner>
        )}
        
        {!loading && perfumes.length === 0 && (
          <EmptyState>
            <h3>No perfumes yet</h3>
            <p>Start by searching for your favorite designer brand!</p>
          </EmptyState>
        )}
        
        {perfumes.length > 0 && (
          <PerfumeGrid>
            {perfumes.map((perfume) => (
              <PerfumeCard
                key={perfume.id}
                perfume={perfume}
                onDelete={handleDelete}
              />
            ))}
          </PerfumeGrid>
        )}
      </MainContent>
    </AppContainer>
  );
};

export default App;
