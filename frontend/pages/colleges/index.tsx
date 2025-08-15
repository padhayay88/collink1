import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import {
  Box,
  Container,
  Heading,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  SimpleGrid,
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Text,
  Badge,
  Input,
  InputGroup,
  InputLeftElement,
  Select,
  Stack,
  Button,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  VStack,
  HStack,
  Divider,
  Spinner,
  useToast,
} from '@chakra-ui/react';
import { loadCollegeCache, getCollegeName } from '../../lib/collegeCache';
import { FiSearch, FiFilter, FiMapPin, FiAward, FiList } from 'react-icons/fi';

interface College {
  id?: string;
  name: string;
  state?: string;
  rank?: number | string;
  category?: string;
  exam_type?: string;
  annual_fees?: string | number;
  ownership?: string;
  website?: string;
  address?: string;
  [key: string]: any;
}

interface CollegeData {
  by_rank: Record<string, College[]>;
  by_state: Record<string, College[]>;
  by_category: Record<string, College[]>;
}

export default function CollegesPage() {
  const router = useRouter();
  const toast = useToast();
  const [loading, setLoading] = useState(true);
  const [collegeData, setCollegeData] = useState<CollegeData>({
    by_rank: {},
    by_state: {},
    by_category: {}
  });
  const [activeTab, setActiveTab] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedState, setSelectedState] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedCollege, setSelectedCollege] = useState<College | null>(null);
  const { isOpen, onOpen, onClose } = useDisclosure();
  // At-rank query state (SQL-backed)
  const [rankInput, setRankInput] = useState<string>('');
  const [examInput, setExamInput] = useState<string>('jee main');
  const [categoryInput, setCategoryInput] = useState<string>('');
  const [yearInput, setYearInput] = useState<string>('');
  const [toleranceInput, setToleranceInput] = useState<string>('0');
  const [statesInput, setStatesInput] = useState<string>('');
  const [ownershipInput, setOwnershipInput] = useState<string>('');
  const [includeNoRank, setIncludeNoRank] = useState<boolean>(true);
  const [atRankLoading, setAtRankLoading] = useState<boolean>(false);
  const [atRankResults, setAtRankResults] = useState<College[]>([]);

  // Fetch college data
  useEffect(() => {
    const fetchColleges = async () => {
      try {
        setLoading(true);
        // Preload cache so names can be filled if API rows miss them
        loadCollegeCache().catch(() => {});
        // In a real app, you would fetch this from your API
        const [rankRes, stateRes, categoryRes] = await Promise.all([
          fetch('/api/colleges/rank'),
          fetch('/api/colleges/state'),
          fetch('/api/colleges/category')
        ]);

        const by_rank = await rankRes.json();
        const by_state = await stateRes.json();
        const by_category = await categoryRes.json();

        setCollegeData({ by_rank, by_state, by_category });
      } catch (error) {
        console.error('Error fetching college data:', error);
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

    fetchColleges();
  }, [toast]);

  // Filter colleges based on search and filters
  const filterColleges = (colleges: College[]) => {
    return colleges.filter(college => {
      const matchesSearch = college.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         (college.state && college.state.toLowerCase().includes(searchQuery.toLowerCase()));
      
      const matchesState = !selectedState || college.state === selectedState;
      const matchesCategory = !selectedCategory || college.category === selectedCategory;
      
      return matchesSearch && matchesState && matchesCategory;
    });
  };

  // Handle college card click
  const handleCollegeClick = (college: College) => {
    setSelectedCollege(college);
    onOpen();
  };

  // Get all unique states for filter
  const allStates = [...Object.entries(collegeData.by_state).map(([state]) => state)].sort();
  
  // Get all unique categories for filter
  const allCategories = [...Object.entries(collegeData.by_category).map(([category]) => category)].sort();

  // Reset filters
  const resetFilters = () => {
    setSearchQuery('');
    setSelectedState('');
    setSelectedCategory('');
  };

  // Fetch colleges at a particular rank from backend SQL
  const fetchAtRank = async () => {
    if (!rankInput) {
      toast({ title: 'Enter rank', description: 'Please input a rank number', status: 'warning', duration: 3000, isClosable: true });
      return;
    }
    try {
      setAtRankLoading(true);
      const params = new URLSearchParams({ rank: String(rankInput) });
      if (examInput) params.set('exam', examInput);
      if (categoryInput) params.set('category', categoryInput);
      if (yearInput) params.set('year', yearInput);
      if (toleranceInput) params.set('tolerance_percent', toleranceInput);
      if (statesInput) params.set('states', statesInput);
      if (ownershipInput) params.set('ownership', ownershipInput);
      params.set('include_no_rank', String(includeNoRank));
      params.set('limit', '200');
      const res = await fetch(`/api/colleges/at-rank?${params.toString()}`);
      if (!res.ok) {
        const err = await res.text();
        throw new Error(err);
      }
      const data = await res.json();
      // Ensure cache is loaded, then set results with fallback names
      await loadCollegeCache();
      const enriched = (data.colleges || []).map((r: any) => ({
        ...r,
        name: r.name || getCollegeName(r.id, 'College') || 'College',
      }));
      setAtRankResults(enriched);
      if ((data.total || 0) === 0) {
        toast({ title: 'No results', description: 'No colleges found for the given criteria', status: 'info', duration: 3000, isClosable: true });
      }
      // Switch to By Rank tab for consistency
      setActiveTab(0);
    } catch (e: any) {
      console.error('at-rank fetch failed', e);
      toast({ title: 'Error', description: 'Failed to fetch colleges at rank', status: 'error', duration: 4000, isClosable: true });
    } finally {
      setAtRankLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minH="70vh">
        <Spinner size="xl" />
      </Box>
    );
  }

  return (
    <Container maxW="container.xl" py={8}>
      <Head>
        <title>Colleges | Collink</title>
        <meta name="description" content="Browse colleges by rank, state, and category" />
      </Head>

      <Heading as="h1" size="xl" mb={8} textAlign="center">
        Browse Colleges
      </Heading>

      {/* Search and Filters */}
      <Box mb={8} p={4} bg="white" borderRadius="lg" boxShadow="sm">
        <Stack direction={['column', 'row']} spacing={4} mb={4}>
          <InputGroup>
            <InputLeftElement pointerEvents="none">
              <FiSearch color="gray.400" />
            </InputLeftElement>
            <Input
              placeholder="Search colleges..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </InputGroup>
          <Select
            placeholder="Filter by state"
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
            maxW={['100%', '200px']}
          >
            {allStates.map((state) => (
              <option key={state} value={state}>
                {state}
              </option>
            ))}
          </Select>
          <Select
            placeholder="Filter by category"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            maxW={['100%', '200px']}
          >
            {allCategories.map((category) => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </Select>
          <Button onClick={resetFilters} variant="outline">
            Reset Filters
          </Button>
        </Stack>

        {/* At-Rank finder (SQL-backed) */}
        <Divider my={4} />
        <Stack direction={['column', 'row']} spacing={4}>
          <Input type="number" placeholder="Enter your rank" value={rankInput} onChange={(e) => setRankInput(e.target.value)} maxW={["100%", "180px"]} />
          <HStack>
            <Button variant={examInput === 'jee main' ? 'solid' : 'outline'} colorScheme="blue" onClick={() => setExamInput('jee main')}>JEE Main</Button>
            <Button variant={examInput === 'jee advanced' ? 'solid' : 'outline'} colorScheme="blue" onClick={() => setExamInput('jee advanced')}>JEE Advanced</Button>
            <Button variant={examInput === 'cat' ? 'solid' : 'outline'} colorScheme="teal" onClick={() => setExamInput('cat')}>CAT (MBA)</Button>
          </HStack>
          <Input placeholder="Category (e.g., General)" value={categoryInput} onChange={(e) => setCategoryInput(e.target.value)} maxW={["100%", "200px"]} />
          <Input type="number" placeholder="Year (e.g., 2024)" value={yearInput} onChange={(e) => setYearInput(e.target.value)} maxW={["100%", "160px"]} />
          <Input type="number" placeholder="Tolerance % (e.g., 5)" value={toleranceInput} onChange={(e) => setToleranceInput(e.target.value)} maxW={["100%", "200px"]} />
          <Input placeholder="States (comma-separated)" value={statesInput} onChange={(e) => setStatesInput(e.target.value)} />
          <Select placeholder="Ownership (any)" value={ownershipInput} onChange={(e) => setOwnershipInput(e.target.value)} maxW={["100%", "200px"]}>
            <option value="government">Government</option>
            <option value="private">Private</option>
          </Select>
          <HStack>
            <input type="checkbox" checked={includeNoRank} onChange={(e) => setIncludeNoRank(e.target.checked)} />
            <Text>Include colleges without rank</Text>
          </HStack>
          <Button colorScheme="blue" onClick={fetchAtRank} isLoading={atRankLoading}>
            Find at Rank
          </Button>
        </Stack>
        {atRankResults.length > 0 && (
          <Box mt={6}>
            <Heading as="h2" size="md" mb={3}>Results at Rank</Heading>
            <SimpleGrid columns={[1, 2, 3]} spacing={4}>
              {atRankResults.map((r, idx) => (
                <CollegeCard key={`at-rank-${idx}`} college={{
                  name: r.name || getCollegeName((r as any).id, 'College') || 'College',
                  state: r.state,
                  category: r.category,
                  exam_type: r.exam_type,
                  rank: (r as any).closing_rank ?? (r as any).opening_rank,
                  ownership: (r as any).ownership,
                }} onClick={() => handleCollegeClick(r)} />
              ))}
            </SimpleGrid>
          </Box>
        )}
      </Box>

      {/* Tabs */}
      <Tabs variant="enclosed" isFitted onChange={(index) => setActiveTab(index)}>
        <TabList mb={4}>
          <Tab>
            <HStack spacing={2}>
              <FiAward />
              <Text>By Rank</Text>
            </HStack>
          </Tab>
          <Tab>
            <HStack spacing={2}>
              <FiMapPin />
              <Text>By State</Text>
            </HStack>
          </Tab>
          <Tab>
            <HStack spacing={2}>
              <FiList />
              <Text>By Category</Text>
            </HStack>
          </Tab>
        </TabList>

        <TabPanels>
          {/* By Rank */}
          <TabPanel p={0}>
            {Object.entries(collegeData.by_rank).map(([rankRange, colleges]) => {
              const filteredColleges = filterColleges(colleges);
              if (filteredColleges.length === 0) return null;
              
              return (
                <Box key={rankRange} mb={8}>
                  <Heading as="h2" size="md" mb={4}>
                    Rank {rankRange} ({filteredColleges.length} colleges)
                  </Heading>
                  <SimpleGrid columns={[1, 2, 3]} spacing={4}>
                    {filteredColleges.map((college, index) => (
                      <CollegeCard 
                        key={`${rankRange}-${index}`} 
                        college={college} 
                        onClick={() => handleCollegeClick(college)}
                      />
                    ))}
                  </SimpleGrid>
                </Box>
              );
            })}
          </TabPanel>

          {/* By State */}
          <TabPanel p={0}>
            {Object.entries(collegeData.by_state)
              .sort(([stateA], [stateB]) => stateA.localeCompare(stateB))
              .map(([state, colleges]) => {
                const filteredColleges = filterColleges(colleges);
                if (filteredColleges.length === 0) return null;
                
                return (
                  <Box key={state} mb={8}>
                    <Heading as="h2" size="md" mb={4}>
                      {state} ({filteredColleges.length} colleges)
                    </Heading>
                    <SimpleGrid columns={[1, 2, 3]} spacing={4}>
                      {filteredColleges.map((college, index) => (
                        <CollegeCard 
                          key={`${state}-${index}`} 
                          college={college}
                          onClick={() => handleCollegeClick(college)}
                        />
                      ))}
                    </SimpleGrid>
                  </Box>
                );
              })}
          </TabPanel>

          {/* By Category */}
          <TabPanel p={0}>
            {Object.entries(collegeData.by_category).map(([category, colleges]) => {
              const filteredColleges = filterColleges(colleges);
              if (filteredColleges.length === 0) return null;
              
              return (
                <Box key={category} mb={8}>
                  <Heading as="h2" size="md" mb={4}>
                    {category} ({filteredColleges.length} colleges)
                  </Heading>
                  <SimpleGrid columns={[1, 2, 3]} spacing={4}>
                    {filteredColleges.map((college, index) => (
                      <CollegeCard 
                        key={`${category}-${index}`} 
                        college={college}
                        onClick={() => handleCollegeClick(college)}
                      />
                    ))}
                  </SimpleGrid>
                </Box>
              );
            })}
          </TabPanel>
        </TabPanels>
      </Tabs>

      {/* College Detail Modal */}
      <Modal isOpen={isOpen} onClose={onClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          {selectedCollege && (
            <>
              <ModalHeader>{selectedCollege.name}</ModalHeader>
              <ModalCloseButton />
              <ModalBody>
                <VStack spacing={4} align="stretch">
                  {selectedCollege.rank && (
                    <Box>
                      <Text fontWeight="bold">Rank:</Text>
                      <Text>{selectedCollege.rank}</Text>
                    </Box>
                  )}
                  {selectedCollege.state && (
                    <Box>
                      <Text fontWeight="bold">State:</Text>
                      <Text>{selectedCollege.state}</Text>
                    </Box>
                  )}
                  {selectedCollege.category && (
                    <Box>
                      <Text fontWeight="bold">Category:</Text>
                      <Text>{selectedCollege.category}</Text>
                    </Box>
                  )}
                  {selectedCollege.exam_type && (
                    <Box>
                      <Text fontWeight="bold">Exam Type:</Text>
                      <Text>{selectedCollege.exam_type}</Text>
                    </Box>
                  )}
                  {selectedCollege.annual_fees && (
                    <Box>
                      <Text fontWeight="bold">Annual Fees:</Text>
                      <Text>₹{selectedCollege.annual_fees.toLocaleString()}</Text>
                    </Box>
                  )}
                  {selectedCollege.website && (
                    <Box>
                      <Text fontWeight="bold">Website:</Text>
                      <a 
                        href={selectedCollege.website.startsWith('http') ? selectedCollege.website : `https://${selectedCollege.website}`} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        style={{ color: '#3182ce' }}
                      >
                        {selectedCollege.website}
                      </a>
                    </Box>
                  )}
                  {selectedCollege.address && (
                    <Box>
                      <Text fontWeight="bold">Address:</Text>
                      <Text>{selectedCollege.address}</Text>
                    </Box>
                  )}
                </VStack>
              </ModalBody>
              <ModalFooter>
                <Button colorScheme="blue" mr={3} onClick={onClose}>
                  Close
                </Button>
                <Button 
                  variant="outline" 
                  onClick={() => {
                    // Navigate to college detail page if available
                    if (selectedCollege.id) {
                      router.push(`/colleges/${selectedCollege.id}`);
                    } else {
                      // Fallback to search
                      router.push(`/search?q=${encodeURIComponent(selectedCollege.name)}`);
                    }
                  }}
                >
                  View Details
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </Container>
  );
}

// College Card Component
const CollegeCard = ({ college, onClick }: { college: College; onClick: () => void }) => {
  return (
    <Card 
      onClick={onClick}
      cursor="pointer"
      _hover={{
        transform: 'translateY(-4px)',
        boxShadow: 'lg',
        transition: 'all 0.2s',
      }}
      height="100%"
      display="flex"
      flexDirection="column"
    >
      <CardHeader pb={2}>
        <Heading size="md">{college.name}</Heading>
      </CardHeader>
      <CardBody pt={0} pb={4} flexGrow={1}>
        <VStack spacing={2} align="stretch">
          {college.rank && (
            <HStack>
              <Text fontWeight="semibold">Rank:</Text>
              <Text>{college.rank}</Text>
            </HStack>
          )}
          {college.state && (
            <HStack>
              <FiMapPin />
              <Text>{college.state}</Text>
            </HStack>
          )}
          {college.ownership && (
            <HStack>
              <Text fontWeight="semibold">Ownership:</Text>
              <Text textTransform="capitalize">{String(college.ownership)}</Text>
            </HStack>
          )}
          {college.category && (
            <HStack>
              <FiList />
              <Text>{college.category}</Text>
            </HStack>
          )}
          {college.annual_fees && (
            <HStack>
              <Text fontWeight="semibold">Fees:</Text>
              <Text>₹{college.annual_fees.toLocaleString()}/year</Text>
            </HStack>
          )}
        </VStack>
      </CardBody>
      <CardFooter pt={0}>
        <Button 
          size="sm" 
          colorScheme="blue" 
          variant="outline" 
          onClick={(e) => {
            e.stopPropagation();
            onClick();
          }}
        >
          View Details
        </Button>
      </CardFooter>
    </Card>
  );
};
