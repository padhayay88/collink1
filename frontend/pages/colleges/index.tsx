import { useState, useEffect, useRef, useCallback } from 'react';
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
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Checkbox,
  Wrap,
  WrapItem,
  Tag,
  TagLabel,
  TagCloseButton,
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
  const [toleranceInput, setToleranceInput] = useState<string>('5');
  const [ownershipInput, setOwnershipInput] = useState<string>('');
  const [includeNoRank, setIncludeNoRank] = useState<boolean>(false);
  const [atRankLoading, setAtRankLoading] = useState<boolean>(false);
  const [atRankResults, setAtRankResults] = useState<College[]>([]);
  const [atRankOffset, setAtRankOffset] = useState<number>(0);
  const [atRankHasMore, setAtRankHasMore] = useState<boolean>(false);
  const atRankPageSize = 500;
  const sentinelRef = useRef<HTMLDivElement | null>(null);
  // Simple branch filter for at-rank results
  const [branchFilter, setBranchFilter] = useState<string>('');
  // Multi-select States for At-Rank
  const [statesSelected, setStatesSelected] = useState<string[]>([]);
  const [statesQuery, setStatesQuery] = useState<string>('');

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

  // Load next page for at-rank
  const fetchAtRankNext = useCallback(async () => {
    // guard: avoid overlapping loads
    if (atRankLoading || !atRankHasMore) return;
    const currentOffset = atRankOffset;
    try {
      setAtRankLoading(true);
      const asNumber = Number(rankInput);
      // Build states CSV from multi-select or top selectedState
      const statesCsv = statesSelected.length > 0
        ? statesSelected.join(',')
        : (selectedState ? selectedState : '');
      // CAT percentile branch supports pagination with limit/offset if backend supports it; safe to pass anyway
      if (examInput.toLowerCase() === 'cat' && !isNaN(asNumber) && asNumber > 0 && asNumber <= 100) {
        const p = new URLSearchParams({ percentile: String(asNumber) });
        if (yearInput) p.set('year', yearInput);
        if (statesCsv) p.set('states', statesCsv);
        if (ownershipInput) p.set('ownership', ownershipInput);
        if (toleranceInput) p.set('tolerance_percent', toleranceInput);
        // Send top selectedCategory for consistency (backend may ignore for CAT endpoint)
        const effectiveCategory = (categoryInput || selectedCategory || '').trim();
        if (effectiveCategory) p.set('category', effectiveCategory);
        p.set('limit', String(atRankPageSize));
        p.set('offset', String(currentOffset));
        const mbaUrl = `/api/colleges/mba-by-percentile?${p.toString()}`;
        console.log('At-Rank CAT request:', mbaUrl);
        const res = await fetch(mbaUrl, { cache: 'no-store' });
        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();
        await loadCollegeCache();
        const page = (data.colleges || []).map((r: any) => ({
          ...r,
          name: r.name || getCollegeName(r.id, 'College') || 'College',
        }));
        setAtRankResults(prev => [...prev, ...page]);
        setAtRankOffset(currentOffset + atRankPageSize);
        setAtRankHasMore(page.length === atRankPageSize);
        setActiveTab(0);
        return;
      }

      const params = new URLSearchParams({ rank: String(rankInput) });
      if (examInput) params.set('exam', examInput);
      const effectiveCategory2 = (categoryInput || selectedCategory || '').trim();
      if (effectiveCategory2) params.set('category', effectiveCategory2);
      if (yearInput) params.set('year', yearInput);
      if (toleranceInput) {
        params.set('tolerance_percent', toleranceInput);
        const tol = Number(toleranceInput);
        const rnk = Number(rankInput);
        if (!isNaN(tol) && tol >= 0 && !isNaN(rnk) && rnk > 0) {
          const delta = Math.max(1, Math.round((rnk * tol) / 100));
          const minR = Math.max(1, rnk - delta);
          const maxR = rnk + delta;
          params.set('min_rank', String(minR));
          params.set('max_rank', String(maxR));
        }
      }
      if (statesCsv) params.set('states', statesCsv);
      if (ownershipInput) params.set('ownership', ownershipInput);
      params.set('include_no_rank', String(includeNoRank));
      // Always use centered tolerance window handled by backend; avoid static min_rank mode
      params.set('limit', String(atRankPageSize));
      params.set('offset', String(currentOffset));
      const url = `/api/colleges/at-rank?${params.toString()}`;
      console.log('At-Rank request:', url);
      const res = await fetch(url, { cache: 'no-store' });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      await loadCollegeCache();
      const page = (data.colleges || []).map((r: any) => ({
        ...r,
        name: r.name || getCollegeName(r.id, 'College') || 'College',
      }));
      setAtRankResults(prev => [...prev, ...page]);
      setAtRankOffset(currentOffset + atRankPageSize);
      setAtRankHasMore(page.length === atRankPageSize);
      setActiveTab(0);
    } catch (e) {
      console.error('at-rank next page failed', e);
      setAtRankHasMore(false);
      toast({ title: 'Error', description: 'Failed to load more results', status: 'error', duration: 4000, isClosable: true });
    } finally {
      setAtRankLoading(false);
    }
  }, [atRankLoading, atRankHasMore, atRankOffset, rankInput, examInput, categoryInput, yearInput, toleranceInput, ownershipInput, includeNoRank, atRankPageSize, toast, statesSelected, selectedState, selectedCategory]);

  // Fetch colleges at a particular rank from backend SQL (initial load)
  const fetchAtRank = async () => {
    if (!rankInput) {
      toast({ title: 'Enter rank', description: 'Please input a rank number', status: 'warning', duration: 3000, isClosable: true });
      return;
    }
    try {
      // reset paging & results
      setAtRankResults([]);
      setAtRankOffset(0);
      setAtRankHasMore(true);
      await fetchAtRankNext();
    } catch (e: any) {
      console.error('at-rank fetch failed', e);
      toast({ title: 'Error', description: 'Failed to fetch colleges at rank', status: 'error', duration: 4000, isClosable: true });
    } finally {
      // loading state handled inside fetchAtRankNext
    }
  };

  // IntersectionObserver to auto-load more when sentinel visible
  useEffect(() => {
    const el = sentinelRef.current;
    if (!el) return;
    const observer = new IntersectionObserver((entries) => {
      const entry = entries[0];
      if (entry.isIntersecting && atRankHasMore && !atRankLoading && atRankResults.length > 0) {
        fetchAtRankNext();
      }
    }, { root: null, rootMargin: '0px', threshold: 1.0 });
    observer.observe(el);
    return () => observer.disconnect();
  }, [fetchAtRankNext, atRankHasMore, atRankLoading, atRankResults.length]);

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

    <Heading as="h1" size="xl" mb={2} textAlign="center">
      Browse Colleges
    </Heading>
    {/* Total and filtered counts summary */}
    <Box textAlign="center" mb={6} color="gray.600">
      {(() => {
        // Helper to build a unique key
        const keyOf = (c: any) => `${(c.name || '').toString().toLowerCase()}|${(c.state || '').toString().toLowerCase()}`;

        // Unfiltered total using state grouping if present
        const totalSet = new Set<string>();
        const byStateEntries = Object.values(collegeData.by_state);
        if (byStateEntries.length > 0) {
          for (const arr of byStateEntries) for (const c of arr) if (c?.name) totalSet.add(keyOf(c));
        } else {
          for (const arr of Object.values(collegeData.by_category)) for (const c of arr) if (c?.name) totalSet.add(keyOf(c));
          for (const arr of Object.values(collegeData.by_rank)) for (const c of arr) if (c?.name) totalSet.add(keyOf(c));
        }

        // Filtered total: apply existing filterColleges logic to avoid double counting
        const filteredSet = new Set<string>();
        if (byStateEntries.length > 0) {
          for (const arr of byStateEntries) {
            const filtered = filterColleges(arr);
            for (const c of filtered) if (c?.name) filteredSet.add(keyOf(c));
          }
        } else {
          for (const arr of Object.values(collegeData.by_category)) {
            const filtered = filterColleges(arr);
            for (const c of filtered) if (c?.name) filteredSet.add(keyOf(c));
          }
          for (const arr of Object.values(collegeData.by_rank)) {
            const filtered = filterColleges(arr);
            for (const c of filtered) if (c?.name) filteredSet.add(keyOf(c));
          }
        }

        const total = totalSet.size;
        const filtered = filteredSet.size;
        return (
          <Text fontSize="sm">
            Total colleges loaded: <b>{total.toLocaleString()}</b>
            {' '}| Matching current filters: <b>{filtered.toLocaleString()}</b>
          </Text>
        );
      })()}
    </Box>
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
          {/* Multi-select for States with search and chips */}
          <Box>
            <Menu closeOnSelect={false}>
              <MenuButton as={Button} variant="outline" maxW={["100%", "260px"]}>
                {statesSelected.length > 0 ? `States (${statesSelected.length} selected)` : 'Select States'}
              </MenuButton>
              <MenuList maxH="320px" overflowY="auto" minW="260px">
                <Box p={2} borderBottom="1px solid" borderColor="gray.100">
                  <Input size="sm" placeholder="Search states..." value={statesQuery} onChange={(e) => setStatesQuery(e.target.value)} />
                </Box>
                {allStates
                  .filter((s) => !statesQuery || s.toLowerCase().includes(statesQuery.toLowerCase()))
                  .map((state) => (
                    <MenuItem key={state} onClick={(e) => e.preventDefault()}>
                      <Checkbox
                        isChecked={statesSelected.includes(state)}
                        onChange={(e) => {
                          if (e.target.checked) setStatesSelected(prev => [...prev, state]);
                          else setStatesSelected(prev => prev.filter(s => s !== state));
                        }}
                        mr={2}
                      />
                      {state}
                    </MenuItem>
                  ))}
                <Box p={2}>
                  <Button size="xs" variant="ghost" onClick={() => setStatesSelected([])}>Clear all</Button>
                </Box>
              </MenuList>
            </Menu>
            {statesSelected.length > 0 && (
              <Wrap mt={2} maxW={["100%", "400px"]}>
                {statesSelected.map((s) => (
                  <WrapItem key={s}>
                    <Tag size="sm" colorScheme="blue">
                      <TagLabel>{s}</TagLabel>
                      <TagCloseButton onClick={() => setStatesSelected(prev => prev.filter(x => x !== s))} />
                    </Tag>
                  </WrapItem>
                ))}
              </Wrap>
            )}
          </Box>
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
            {/* Branch filter for results */}
            <Input
              placeholder="Filter branches (e.g., Computer Science)"
              value={branchFilter}
              onChange={(e) => setBranchFilter(e.target.value)}
              mb={4}
            />
            <SimpleGrid columns={[1, 2, 3]} spacing={4}>
              {atRankResults
                .filter((r: any) => {
                  // Branch filter
                  const b = (r.branch || '').toString().toLowerCase();
                  if (branchFilter && !b.includes(branchFilter.toLowerCase())) return false;
                  // Apply top State filter to At-Rank results (client-side safeguard)
                  if (selectedState && (r.state || '').toString() !== selectedState) return false;
                  if (statesSelected.length > 0 && !statesSelected.includes((r.state || '').toString())) return false;
                  // Apply top Category filter if available (match exact when present)
                  if (selectedCategory) {
                    const rc = (r.category || '').toString().toLowerCase();
                    if (!rc || rc !== selectedCategory.toLowerCase()) return false;
                  }
                  return true;
                })
                .map((r, idx) => (
                  <CollegeCard
                    key={`at-rank-${idx}`}
                    college={{
                      name: (r as any).name || getCollegeName((r as any).id, 'College') || 'College',
                      state: (r as any).state,
                      category: (r as any).category,
                      exam_type: (r as any).exam_type,
                      rank: (r as any).closing_rank ?? (r as any).opening_rank,
                      ownership: (r as any).ownership,
                      branch: (r as any).branch,
                      opening_rank: (r as any).opening_rank,
                      closing_rank: (r as any).closing_rank,
                      year: (r as any).year,
                      quota: (r as any).quota,
                      location: (r as any).location,
                    }}
                    onClick={() => handleCollegeClick(r as any)}
                  />
                ))}
            </SimpleGrid>
            {/* Sentinel for infinite scroll */}
            <Box ref={sentinelRef} textAlign="center" py={4}>
              {atRankLoading ? <Spinner /> : atRankHasMore ? <Text color="gray.500">Scroll to load more…</Text> : <Text color="gray.500">No more results</Text>}
            </Box>
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
        <HStack mt={1} spacing={2} flexWrap="wrap">
          {college.exam_type && <Badge colorScheme="blue" textTransform="capitalize">{college.exam_type}</Badge>}
          {college.category && <Badge colorScheme="purple">{college.category}</Badge>}
          {college.year && <Badge colorScheme="green">{college.year}</Badge>}
        </HStack>
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
          {college.branch && (
            <HStack>
              <FiList />
              <Text>{college.branch}</Text>
            </HStack>
          )}
          {(college.opening_rank != null || college.closing_rank != null) && (
            <HStack>
              <Text fontWeight="semibold">Cutoff:</Text>
              <Text>
                {college.opening_rank != null ? `Opening ${college.opening_rank}` : ''}
                {college.opening_rank != null && college.closing_rank != null ? ' | ' : ''}
                {college.closing_rank != null ? `Closing ${college.closing_rank}` : ''}
              </Text>
            </HStack>
          )}
          {college.quota && (
            <HStack>
              <Text fontWeight="semibold">Quota:</Text>
              <Text>{college.quota}</Text>
            </HStack>
          )}
          {college.location && (
            <HStack>
              <Text fontWeight="semibold">Location:</Text>
              <Text>{String(college.location)}</Text>
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
