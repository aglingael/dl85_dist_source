#ifndef LCMB_H
#define LCMB_H

#include "globals.h"
#include "cache.h"
#include "cache_trie.h"
#include "solution.h"
#include "search_base.h"


class Search_cache : public Search_base{
public:
    Search_cache (NodeDataManager *nodeDataManager,
                  bool infoGain,
                  bool infoAsc,
                  bool repeatSort,
                  Support minsup,
                  Depth maxdepth,
                  Cache *cache,
                  int timeLimit,
                  float maxError = NO_ERR,
                  bool specialAlgo = true,
                  bool stopAfterError = false);

    ~Search_cache();

    void run ();

    Cache *cache;

    /*NodeDataManager *nodeDataManager;
    bool infoGain = false;
    bool infoAsc = false; //if true ==> items with low IG are explored first
    bool repeatSort = false;
    Support minsup;
    Depth maxdepth;
    int timeLimit;
    float maxError = NO_ERR;
    bool stopAfterError = false;
    bool specialAlgo = true;
    bool timeLimitReached = false;*/

private:
    Node* recurse ( Array<Item> itemset, Attribute last_added, Node* node, Array<Attribute> attributes_to_visit, Depth depth, Error ub);
    Array<Attribute> getSuccessors(Array<Attribute> last_freq_attributes, Attribute last_added, Node* node);
    float informationGain ( Supports notTaken, Supports taken);
    Node *getSolutionIfExists(Node *node, Error ub, Depth depth);
//    Array<Attribute> getExistingSuccessors(TrieNode* node);
//    Error computeSimilarityLowerBound(bitset<M> *b1_cover, bitset<M> *b2_cover, Error b1_error, Error b2_error);
//    void addInfoForLowerBound(NodeData *node_data, bitset<M> *&b1_cover, bitset<M> *&b2_cover, Error &b1_error, Error &b2_error, Support &highest_coversize);


};

// a variable to express whether the error computation is performed in python or not
#define is_python_error nodeDataManager->tids_error_callback || nodeDataManager->tids_error_class_callback || nodeDataManager->supports_error_class_callback

#endif