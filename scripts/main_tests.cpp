// my first program in C++
#include <iostream>

enum class PfCand1 {
  pfCand_pt = 0,
  pfCand_eta = 1
};

enum class PfCand2 {
  pfCand_pt = 0,
  pfCand_eta = 1
};

template<typename T> struct FeaturesHelper;
template<> struct FeaturesHelper<PfCand1> {
static constexpr size_t size = 10;
};

template<> struct FeaturesHelper<PfCand2> {
static constexpr size_t size = 15;
};


using FeatureTuple = std::tuple<PfCand1, PfCand2>;

template<typename T, T... ints>
void print_sequence(std::integer_sequence<T, ints...> int_seq)
{
    std::cout << "The sequence of size " << int_seq.size() << ": ";
    ((std::cout << ints << ' '),...);
    std::cout << '\n';
}

template<size_t... I>
std::vector<size_t> CreateStartIndices(const int start0, std::index_sequence<I...> idx_seq)
{

  std::vector<size_t> start(idx_seq.size());
  ((
    using tuple_element =  std::tuple_element_t<I, FeatureTuple>;
    start[I] = FeaturesHelper<tuple_element>::size  + start0 + I
    ), ...);
  return start;
}

void main_tests()
{
  using TestType = std::tuple<int, int>;
  TestType a = std::make_tuple(1, 2);
  std::cout << std::get<0>(a) << std::endl;

  // --------------------------------
  static constexpr size_t nFeaturesTypes = std::tuple_size<FeatureTuple>::value;
  static constexpr size_t nFeaturesTypes_v = std::tuple_size_v<FeatureTuple>; // the same as previous
  std::cout << nFeaturesTypes << " " << nFeaturesTypes_v << std::endl;

  // --------------------------------
  // The class template std::integer_sequence represents a compile-time sequence of integers.
  print_sequence(std::integer_sequence<unsigned, 9, 2, 5, 1, 9, 1, 6>{});
  print_sequence(std::make_integer_sequence<unsigned, 4>{});

  // --------------------------------
} 