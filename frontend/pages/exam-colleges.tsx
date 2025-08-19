import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import {
  Box,
  Container,
  Heading,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Select,
  Input,
  InputGroup,
  InputLeftElement,
  Stack,
  Text,
  SimpleGrid,
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Button,
  Badge,
  useToast,
  Spinner,
} from '@chakra-ui/react';
import { SearchIcon } from '@chakra-ui/icons';

type College = {
  'S.No': number;
  'College Name': string;
  'State/UT': string;
  'Type': string;
  'Exam Type': string;
  'Category': string;
  'Ranking': string;
  'Entrance Exam Cutoff': string;
  'Annual Fees (INR)': string;
  'Seats': string;
  'Established': number;
  'Website': string;
  'Address': string;
  'Contact Email': string;
  'Contact Phone': string;
};

type ExamStats = {
  total_colleges: number;
  states: string[];
  categories: string[];
  top_colleges: College[];
  state_distribution: Record<string, number>;
};

export default function ExamColleges() {
  const router = useRouter();
  const { exam } = router.query;
  const toast = useToast();
  
  const [colleges, setColleges] = useState<College[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<ExamStats | null>(null);
  const [filters, setFilters] = useState({
    state: '',
    category: '',
    minRank: '',
    maxRank: '',
  });

  useEffect(() => {
    if (!exam) return;
    
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch stats
        const statsRes = await fetch(`/api/colleges/stats/${exam}`);
        if (!statsRes.ok) throw new Error('Failed to fetch stats');
        const statsData = await statsRes.json();
        setStats(statsData);
        
        // Fetch colleges
        await fetchColleges();
        
      } catch (error) {
        console.error('Error:', error);
        toast({
          title: 'Error',
          description: 'Failed to load college data',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [exam]);
  
  const fetchColleges = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.state) params.append('state', filters.state);
      if (filters.category) params.append('category', filters.category);
      if (filters.minRank) params.append('min_rank', filters.minRank);
      if (filters.maxRank) params.append('max_rank', filters.maxRank);
      
      const res = await fetch(`/api/colleges/exam/${exam}?${params.toString()}`);
      if (!res.ok) throw new Error('Failed to fetch colleges');
      
      const data = await res.json();
      setColleges(data);
    } catch (error) {
      console.error('Error:', error);
      toast({
        title: 'Error',
        description: 'Failed to fetch colleges',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };
  
  const handleFilterChange = (e: React.ChangeEvent<HTMLSelectElement | HTMLInputElement>) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const handleApplyFilters = () => {
    setLoading(true);
    fetchColleges().finally(() => setLoading(false));
  };
  
  const handleResetFilters = () => {
    setFilters({
      state: '',
      category: '',
      minRank: '',
      maxRank: '',
    });
  };
  
  if (!exam) {
    return (
      <Container maxW="container.xl" py={8}>
        <Text>Loading...</Text>
      </Container>
    );
  }
  
  const examTitle = exam === 'neet' ? 'NEET' : 'JEE';
  
  return (
    <Box bg="gray.50" minH="100vh">
      <Head>
        <title>{examTitle} Colleges | Collink</title>
        <meta name="description" content={`Browse ${examTitle} colleges with rank, cutoff, and other details`} />
      </Head>
      
      <Box bg="blue.600" color="white" py={8}>
        <Container maxW="container.xl">
          <Heading as="h1" size="xl" mb={4}>
            {examTitle} Colleges
          </Heading>
          <Text fontSize="lg">
            Browse and compare {examTitle} colleges across India
          </Text>
        </Container>
      </Box>
      
      <Container maxW="container.xl" py={8}>
        {/* Stats Overview */}
        {stats && (
          <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6} mb={8}>
            <Card>
              <CardHeader>
                <Heading size="md">Total Colleges</Heading>
              </CardHeader>
              <CardBody>
                <Text fontSize="4xl" fontWeight="bold">
                  {stats.total_colleges.toLocaleString()}
                </Text>
              </CardBody>
            </Card>
            
            <Card>
              <CardHeader>
                <Heading size="md">States</Heading>
              </CardHeader>
              <CardBody>
                <Text fontSize="4xl" fontWeight="bold">
                  {stats.states.length}
                </Text>
                <Text fontSize="sm" color="gray.500">
                  {stats.states.slice(0, 3).join(', ')}
                  {stats.states.length > 3 ? '...' : ''}
                </Text>
              </CardBody>
            </Card>
            
            <Card>
              <CardHeader>
                <Heading size="md">Top College</Heading>
              </CardHeader>
              <CardBody>
                <Text fontSize="lg" fontWeight="bold" isTruncated>
                  {stats.top_colleges[0]?.['College Name'] || 'N/A'}
                </Text>
                <Text fontSize="sm" color="gray.500">
                  Rank: {stats.top_colleges[0]?.Ranking || 'N/A'}
                </Text>
              </CardBody>
            </Card>
          </SimpleGrid>
        )}
        
        {/* Filters */}
        <Card mb={8}>
          <CardBody>
            <Stack direction={{ base: 'column', md: 'row' }} spacing={4}>
              <Select
                placeholder="Select State"
                name="state"
                value={filters.state}
                onChange={handleFilterChange}
              >
                {stats?.states.map((state) => (
                  <option key={state} value={state}>
                    {state}
                  </option>
                ))}
              </Select>
              
              <Select
                placeholder="Select Category"
                name="category"
                value={filters.category}
                onChange={handleFilterChange}
              >
                {stats?.categories.map((category) => (
                  <option key={category} value={category}>
                    {category}
                  </option>
                ))}
              </Select>
              
              <Input
                placeholder="Min Rank"
                name="minRank"
                type="number"
                value={filters.minRank}
                onChange={handleFilterChange}
              />
              
              <Input
                placeholder="Max Rank"
                name="maxRank"
                type="number"
                value={filters.maxRank}
                onChange={handleFilterChange}
              />
              
              <Button colorScheme="blue" onClick={handleApplyFilters} isLoading={loading}>
                Apply Filters
              </Button>
              
              <Button variant="outline" onClick={handleResetFilters} isDisabled={loading}>
                Reset
              </Button>
            </Stack>
          </CardBody>
        </Card>
        
        {/* Results */}
        <Card>
          <CardBody>
            {loading ? (
              <Box textAlign="center" py={8}>
                <Spinner size="xl" />
                <Text mt={4}>Loading colleges...</Text>
              </Box>
            ) : colleges.length > 0 ? (
              <Box overflowX="auto">
                <Table variant="simple">
                  <Thead>
                    <Tr>
                      <Th>Rank</Th>
                      <Th>College Name</Th>
                      <Th>State</Th>
                      <Th>Type</Th>
                      <Th>Category</Th>
                      <Th>Cutoff</Th>
                      <Th>Annual Fees (INR)</Th>
                      <Th>Seats</Th>
                    </Tr>
                  </Thead>
                  <Tbody>
                    {colleges.map((college) => (
                      <Tr key={college['S.No']} _hover={{ bg: 'gray.50' }}>
                        <Td fontWeight="bold">{college.Ranking}</Td>
                        <Td fontWeight="medium">{college['College Name']}</Td>
                        <Td>{college['State/UT']}</Td>
                        <Td>{college.Type}</Td>
                        <Td>
                          <Badge colorScheme="blue">
                            {college.Category}
                          </Badge>
                        </Td>
                        <Td>{college['Entrance Exam Cutoff']}</Td>
                        <Td>
                          {parseInt(college['Annual Fees (INR)'] || '0').toLocaleString('en-IN', {
                            style: 'currency',
                            currency: 'INR',
                            maximumFractionDigits: 0,
                          })}
                        </Td>
                        <Td>{college.Seats}</Td>
                      </Tr>
                    ))}
                  </Tbody>
                </Table>
              </Box>
            ) : (
              <Box textAlign="center" py={8}>
                <Text fontSize="lg">No colleges found matching your criteria</Text>
                <Button mt={4} colorScheme="blue" onClick={handleResetFilters}>
                  Clear Filters
                </Button>
              </Box>
            )}
          </CardBody>
        </Card>
      </Container>
    </Box>
  );
}
