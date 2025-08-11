import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';
import { Filter, IndianRupee, Users, MapPin, Star, TrendingUp } from 'lucide-react';

const FeeFilter = () => {
  const [colleges, setColleges] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    minFee: 0,
    maxFee: 600000,
    category: 'general',
    examType: 'engineering',
    limit: 20
  });

  const categories = {
    'general': 'General Category',
    'obc_ncl': 'OBC (Non-Creamy Layer)',
    'sc_st': 'SC/ST',
    'pwd': 'Persons with Disabilities'
  };

  const examTypes = {
    'engineering': 'Engineering Colleges',
    'medical': 'Medical Colleges',
    'all': 'All Colleges'
  };

  const fetchColleges = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        min_fee: filters.minFee.toString(),
        max_fee: filters.maxFee.toString(),
        category: filters.category,
        exam_type: filters.examType,
        limit: filters.limit.toString()
      });

      const response = await fetch(`/api/v1/colleges/fee-filter?${params}`);
      const data = await response.json();
      setColleges(data.colleges || []);
    } catch (error) {
      console.error('Error fetching colleges:', error);
      setColleges([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchColleges();
  }, [filters]);

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount);
  };

  const getCategoryBadgeColor = (category) => {
    switch (category) {
      case 'general': return 'bg-blue-100 text-blue-800';
      case 'obc_ncl': return 'bg-green-100 text-green-800';
      case 'sc_st': return 'bg-purple-100 text-purple-800';
      case 'pwd': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-lg">
        <h1 className="text-3xl font-bold mb-2">College Fee Filter</h1>
        <p className="text-blue-100">Find colleges based on your budget and category</p>
      </div>

      {/* Filter Controls */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Filter className="h-5 w-5" />
            Filter Colleges
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Category Selection */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Category</label>
              <Select value={filters.category} onValueChange={(value) => handleFilterChange('category', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(categories).map(([key, label]) => (
                    <SelectItem key={key} value={key}>
                      {label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Exam Type Selection */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Exam Type</label>
              <Select value={filters.examType} onValueChange={(value) => handleFilterChange('examType', value)}>
                <SelectTrigger>
                  <SelectValue placeholder="Select exam type" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(examTypes).map(([key, label]) => (
                    <SelectItem key={key} value={key}>
                      {label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Limit Selection */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Number of Results</label>
              <Select value={filters.limit.toString()} onValueChange={(value) => handleFilterChange('limit', parseInt(value))}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="10">10 Colleges</SelectItem>
                  <SelectItem value="20">20 Colleges</SelectItem>
                  <SelectItem value="50">50 Colleges</SelectItem>
                  <SelectItem value="100">100 Colleges</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Fee Range Slider */}
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <label className="text-sm font-medium">Annual Fee Range</label>
              <span className="text-sm text-gray-500">
                {formatCurrency(filters.minFee)} - {formatCurrency(filters.maxFee)}
              </span>
            </div>
            <div className="px-4">
              <Slider
                value={[filters.minFee, filters.maxFee]}
                onValueChange={([min, max]) => {
                  handleFilterChange('minFee', min);
                  handleFilterChange('maxFee', max);
                }}
                max={600000}
                min={0}
                step={10000}
                className="w-full"
              />
            </div>
          </div>

          {/* Category Information */}
          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="font-medium text-blue-900 mb-2">Category Benefits:</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li><strong>General & OBC:</strong> Full fee payment required</li>
              <li><strong>SC/ST:</strong> Free tuition and hostel fees (only mess & misc. fees)</li>
              <li><strong>PWD:</strong> Free tuition and hostel fees (only mess & misc. fees)</li>
              <li>Reservation percentages: General (50%), OBC (27%), SC (15%), ST (7.5%), PWD (5%)</li>
            </ul>
          </div>
        </CardContent>
      </Card>

      {/* Results */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">
            {loading ? 'Loading...' : `Found ${colleges.length} colleges`}
          </h2>
          <Badge className={getCategoryBadgeColor(filters.category)}>
            {categories[filters.category]}
          </Badge>
        </div>

        <div className="grid gap-4">
          {colleges.map((college, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{college.name}</h3>
                    <div className="flex items-center gap-4 text-sm text-gray-600 mt-1">
                      <span className="flex items-center gap-1">
                        <MapPin className="h-4 w-4" />
                        {college.location}
                      </span>
                      {college.nirf_rank && (
                        <span className="flex items-center gap-1">
                          <Star className="h-4 w-4" />
                          NIRF Rank: {college.nirf_rank}
                        </span>
                      )}
                      {college.established && (
                        <span>Est. {college.established}</span>
                      )}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-green-600">
                      {formatCurrency(college.total_fee)}
                    </div>
                    <div className="text-sm text-gray-500">per year</div>
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                  {college.fee_breakdown && (
                    <>
                      <div className="text-center p-2 bg-gray-50 rounded">
                        <div className="text-xs text-gray-600">Tuition Fee</div>
                        <div className="font-medium">{formatCurrency(college.fee_breakdown.tuition_fee || 0)}</div>
                      </div>
                      <div className="text-center p-2 bg-gray-50 rounded">
                        <div className="text-xs text-gray-600">Hostel Fee</div>
                        <div className="font-medium">{formatCurrency(college.fee_breakdown.hostel_fee || 0)}</div>
                      </div>
                      <div className="text-center p-2 bg-gray-50 rounded">
                        <div className="text-xs text-gray-600">Mess Fee</div>
                        <div className="font-medium">{formatCurrency(college.fee_breakdown.mess_fee || 0)}</div>
                      </div>
                      <div className="text-center p-2 bg-gray-50 rounded">
                        <div className="text-xs text-gray-600">Other Charges</div>
                        <div className="font-medium">{formatCurrency(college.fee_breakdown.other_charges || 0)}</div>
                      </div>
                    </>
                  )}
                </div>

                <div className="flex justify-between items-center">
                  <div className="flex gap-4 text-sm text-gray-600">
                    {college.placement_percentage && (
                      <span className="flex items-center gap-1">
                        <TrendingUp className="h-4 w-4" />
                        {college.placement_percentage}% Placement
                      </span>
                    )}
                    {college.average_package && (
                      <span className="flex items-center gap-1">
                        <IndianRupee className="h-4 w-4" />
                        Avg Package: {formatCurrency(college.average_package)}
                      </span>
                    )}
                  </div>
                  <Button variant="outline" size="sm">
                    <a href={college.website} target="_blank" rel="noopener noreferrer">
                      View Details
                    </a>
                  </Button>
                </div>

                {college.overview && (
                  <div className="mt-4 pt-4 border-t">
                    <p className="text-sm text-gray-600">{college.overview}</p>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>

        {colleges.length === 0 && !loading && (
          <div className="text-center py-12">
            <div className="text-gray-500 text-lg">No colleges found matching your criteria</div>
            <div className="text-sm text-gray-400 mt-2">Try adjusting your filters</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FeeFilter;
