#include <map>
#include <unordered_set>
#include <boost/algorithm/string.hpp>
#include <boost/filesystem/convenience.hpp>
#include <boost/filesystem.hpp>
#include <boost/regex.hpp>

std::vector<std::string> SplitValueList(const std::string& _values_str, bool allow_duplicates,
                                        const std::string& separators, bool enable_token_compress)
{
    std::string values_str = _values_str;
    std::vector<std::string> result;
    if(enable_token_compress)
        boost::trim_if(values_str, boost::is_any_of(separators));
    if(!values_str.size()) return result;
    const auto token_compress = enable_token_compress ? boost::algorithm::token_compress_on
                                                      : boost::algorithm::token_compress_off;
    boost::split(result, values_str, boost::is_any_of(separators), token_compress);
    if(!allow_duplicates) {
        std::unordered_set<std::string> set_result;
        for(const std::string& value : result) {
            if(set_result.count(value))
                throw std::runtime_error("Value listed more than once in the value list");
            set_result.insert(value);
        }
    }
    return result;
}

void CollectInputFiles(const boost::filesystem::path& dir, std::vector<std::string>& files,
                       const boost::regex& pattern, const std::set<std::string>& exclude,
                       const std::set<std::string>& exclude_dirs)
{
    for(const auto& entry : boost::make_iterator_range(boost::filesystem::directory_iterator(dir), {})) {
        if(boost::filesystem::is_directory(entry)
                && !exclude_dirs.count(entry.path().filename().string()))
            CollectInputFiles(entry.path(), files, pattern, exclude, exclude_dirs);
        else if(boost::regex_match(entry.path().string(), pattern)
                && !exclude.count(entry.path().filename().string()))
            files.push_back(entry.path().string());
    }
}

std::vector<std::string> FindInputFiles(const std::vector<std::string>& dirs,
                                               const std::string& file_name_pattern,
                                               const std::string& exclude_list,
                                               const std::string& exclude_dir_list)
{
    auto exclude_vector = SplitValueList(exclude_list, true, ",", true);
    std::set<std::string> exclude(exclude_vector.begin(), exclude_vector.end());

    auto exclude_dir_vector = SplitValueList(exclude_dir_list, true, ",", true);
    std::set<std::string> exclude_dirs(exclude_dir_vector.begin(), exclude_dir_vector.end());

    const boost::regex pattern(file_name_pattern);
    std::vector<std::string> files;
    for(const auto& dir : dirs) {
        boost::filesystem::path path(dir);
        CollectInputFiles(path, files, pattern, exclude, exclude_dirs);
    }
    return files;
}
