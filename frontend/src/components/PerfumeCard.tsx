import React, { useState } from 'react';
import styled from 'styled-components';
import { 
  Trash2, 
  ExternalLink, 
  Package, 
  DollarSign, 
  Calendar,
  Star,
  Clock,
  Wind,
  Info,
  ChevronDown,
  ChevronUp,
  Flower2
} from 'lucide-react';
import Skeleton, { SkeletonTheme } from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';
import { Perfume } from '../types/perfume';

const Card = styled.div`
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  position: relative;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.15);
  }
`;

const ImageContainer = styled.div`
  position: relative;
  height: 200px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  overflow: hidden;
`;

const PerfumeImage = styled.img`
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
  
  ${Card}:hover & {
    transform: scale(1.05);
  }
`;

const PlaceholderImage = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  color: #666;
`;

const GenderBadge = styled.div<{ gender?: string | null }>`
  position: absolute;
  top: 10px;
  right: 10px;
  background: ${props => {
    if (props.gender === 'Women') return 'linear-gradient(135deg, #ff6b9d 0%, #c44569 100%)';
    if (props.gender === 'Men') return 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)';
    return 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)';
  }};
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
`;

const YearBadge = styled.div`
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 6px 10px;
  border-radius: 15px;
  font-size: 0.75rem;
  font-weight: 600;
  backdrop-filter: blur(5px);
`;

const RatingBadge = styled.div`
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: linear-gradient(135deg, #ffd700 0%, #ffaa00 100%);
  color: #333;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 1rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
`;

const Content = styled.div`
  padding: 20px;
`;

const Header = styled.div`
  margin-bottom: 15px;
`;

const Brand = styled.div`
  color: #667eea;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 5px;
`;

const Name = styled.h3`
  color: #333;
  font-size: 1.2rem;
  margin: 0;
  line-height: 1.3;
  font-weight: 700;
`;

const InfoGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 15px;
`;

const InfoItem = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 0.9rem;
`;

const Price = styled.div`
  font-size: 1.5rem;
  font-weight: 700;
  color: #27ae60;
  margin-bottom: 15px;
  
  span {
    font-size: 0.9rem;
    color: #666;
    font-weight: 400;
  }
`;

const Actions = styled.div`
  display: flex;
  gap: 10px;
`;

const Button = styled.button`
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 16px;
  border: none;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const ViewButton = styled(Button)`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
  }
`;

const DeleteButton = styled(Button)`
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 107, 107, 0.3);
  }
`;

const ExpandButton = styled(Button)`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin-top: 15px;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
  }
`;

const LoadingOverlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  z-index: 10;
`;

const NoPrice = styled.div`
  color: #999;
  font-style: italic;
  font-size: 1.1rem;
  margin-bottom: 15px;
`;

const DateInfo = styled.div`
  color: #999;
  font-size: 0.75rem;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #eee;
`;

const NotesSection = styled.div`
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
`;

const NotesTitle = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  color: #667eea;
  font-weight: 600;
  margin-bottom: 10px;
  font-size: 0.95rem;
`;

const NoteLayer = styled.div`
  margin-bottom: 12px;
  
  &:last-child {
    margin-bottom: 0;
  }
`;

const NoteLabel = styled.div`
  font-weight: 600;
  color: #333;
  font-size: 0.85rem;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const NoteValue = styled.div`
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
`;

const Characteristics = styled.div`
  display: flex;
  gap: 15px;
  margin-top: 10px;
`;

const Characteristic = styled.div`
  display: flex;
  align-items: center;
  gap: 6px;
  color: #666;
  font-size: 0.85rem;
  
  svg {
    color: #667eea;
  }
`;

interface PerfumeCardProps {
  perfume: Perfume;
  onDelete: (id: number) => void;
}

const PerfumeCard: React.FC<PerfumeCardProps> = ({ perfume, onDelete }) => {
  const [isDeleting, setIsDeleting] = useState(false);
  const [imageError, setImageError] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this perfume?')) {
      setIsDeleting(true);
      try {
        await onDelete(perfume.id);
      } catch (error) {
        console.error('Error deleting perfume:', error);
        setIsDeleting(false);
      }
    }
  };

  const handleViewSource = () => {
    if (perfume.source_url) {
      window.open(perfume.source_url, '_blank');
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  const hasNotes = perfume.top_notes || perfume.middle_notes || perfume.base_notes;
  const hasCharacteristics = perfume.longevity || perfume.sillage;

  return (
    <Card>
      {isDeleting && (
        <LoadingOverlay>
          <div>Deleting...</div>
        </LoadingOverlay>
      )}
      
      <ImageContainer>
        {perfume.image_url && !imageError ? (
          <PerfumeImage
            src={perfume.image_url}
            alt={perfume.name}
            onError={() => setImageError(true)}
          />
        ) : (
          <PlaceholderImage>
            <Package size={48} />
          </PlaceholderImage>
        )}
        
        {perfume.gender && (
          <GenderBadge gender={perfume.gender}>
            {perfume.gender}
          </GenderBadge>
        )}
        
        {perfume.year && (
          <YearBadge>{perfume.year}</YearBadge>
        )}
        
        {perfume.rating && (
          <RatingBadge>
            <Star size={16} fill="currentColor" />
            {perfume.rating.toFixed(1)}
          </RatingBadge>
        )}
      </ImageContainer>
      
      <Content>
        <Header>
          <Brand>{perfume.brand}</Brand>
          <Name>{perfume.name}</Name>
        </Header>
        
        <InfoGrid>
          <InfoItem>
            <Package size={16} />
            {perfume.size || 'Size not specified'}
          </InfoItem>
          <InfoItem>
            <Calendar size={16} />
            Added {formatDate(perfume.created_at)}
          </InfoItem>
        </InfoGrid>
        
        {perfume.price ? (
          <Price>
            ${perfume.price.toFixed(2)}
            {perfume.size && <span> • {perfume.size}</span>}
          </Price>
        ) : (
          <NoPrice>Price not available</NoPrice>
        )}
        
        {hasCharacteristics && (
          <Characteristics>
            {perfume.longevity && (
              <Characteristic>
                <Clock size={14} />
                {perfume.longevity}
              </Characteristic>
            )}
            {perfume.sillage && (
              <Characteristic>
                <Wind size={14} />
                {perfume.sillage}
              </Characteristic>
            )}
          </Characteristics>
        )}
        
        {perfume.description && (
          <div style={{ 
            color: '#666', 
            fontSize: '0.9rem', 
            lineHeight: 1.4, 
            marginTop: '15px',
            display: '-webkit-box',
            WebkitLineClamp: isExpanded ? undefined : 2,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden'
          }}>
            {perfume.description}
          </div>
        )}
        
        {isExpanded && hasNotes && (
          <NotesSection>
            <NotesTitle>
              <Flower2 size={18} />
              Fragrance Notes
            </NotesTitle>
            
            {perfume.top_notes && (
              <NoteLayer>
                <NoteLabel>Top Notes</NoteLabel>
                <NoteValue>{perfume.top_notes}</NoteValue>
              </NoteLayer>
            )}
            
            {perfume.middle_notes && (
              <NoteLayer>
                <NoteLabel>Middle Notes</NoteLabel>
                <NoteValue>{perfume.middle_notes}</NoteValue>
              </NoteLayer>
            )}
            
            {perfume.base_notes && (
              <NoteLayer>
                <NoteLabel>Base Notes</NoteLabel>
                <NoteValue>{perfume.base_notes}</NoteValue>
              </NoteLayer>
            )}
          </NotesSection>
        )}
        
        {(hasNotes || perfume.description) && (
          <ExpandButton onClick={() => setIsExpanded(!isExpanded)}>
            {isExpanded ? (
              <>
                <ChevronUp size={16} />
                Show Less
              </>
            ) : (
              <>
                <ChevronDown size={16} />
                Show {hasNotes ? 'Notes & ' : ''}Details
              </>
            )}
          </ExpandButton>
        )}
        
        <Actions>
          <ViewButton
            onClick={handleViewSource}
            disabled={!perfume.source_url}
          >
            <ExternalLink size={16} />
            View
          </ViewButton>
          <DeleteButton
            onClick={handleDelete}
            disabled={isDeleting}
          >
            <Trash2 size={16} />
            Delete
          </DeleteButton>
        </Actions>
        
        <DateInfo>
          Source: {perfume.source_url ? new URL(perfume.source_url).hostname : 'Database'}
        </DateInfo>
      </Content>
    </Card>
  );
};

const PerfumeCardSkeleton: React.FC = () => (
  <SkeletonTheme baseColor="#f0f0f0" highlightColor="#e0e0e0">
    <Card>
      <Skeleton height={200} />
      <Content>
        <Skeleton height={20} width={100} style={{ marginBottom: '5px' }} />
        <Skeleton height={25} width="80%" style={{ marginBottom: '15px' }} />
        <InfoGrid>
          <Skeleton height={16} width={80} />
          <Skeleton height={16} width={80} />
        </InfoGrid>
        <Skeleton height={30} width={120} style={{ marginBottom: '15px' }} />
        <Skeleton height={40} width="100%" style={{ marginBottom: '15px' }} />
        <Actions>
          <div style={{ flex: 1, marginRight: '10px' }}>
            <Skeleton height={40} width="100%" />
          </div>
          <div style={{ flex: 1 }}>
            <Skeleton height={40} width="100%" />
          </div>
        </Actions>
      </Content>
    </Card>
  </SkeletonTheme>
);

export { PerfumeCardSkeleton };
export default PerfumeCard;
