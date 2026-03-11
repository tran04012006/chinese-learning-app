#include <iostream>
#include <queue>
#include <vector>
#include <algorithm> // Thư viện cần thiết

using namespace std;

class Solution
{
public:
    vector<int> getAverages(vector<int>& nums, int k)
    {
        long long n = nums.size();

        if (k == 0)
            return nums;
        vector<int> avgs(n, -1);
        if (k > n)
        {
            return avgs;
        }
        //tạo prefix_sum
        long long prefix_sum[n+1];
        prefix_sum[0] = 0;
        for (long long i=1 ; i < n+1 ; i++)
        {
            prefix_sum[i] = prefix_sum[i-1] + nums[i-1];
        }
        for (long long i=k ; i<n-k ; i++)
        {
            long long left = i-k;
            long long right = i + k;
            long long sum = prefix_sum[right+1] - prefix_sum[left];
            long long windowSize = 2*k + 1;
            long long avg = sum / windowSize;
            avgs[i] = avg;
        }
        return avgs;
    }
};

int main()
{
    Solution ans;
    vector<int> s = {7,4,3,9,1,8,5,2,6};
    int k = 3;
    ans.getAverages(s,k);
}
