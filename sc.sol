pragma experimental ABIEncoderV2;

contract AssetTracking {

    struct CheckIn{
        address checker;
        string location;
        uint datetime;
        bytes32 assetId;
        bytes32 checkId;
    }

    struct Asset{
        bytes32 id;
        address creator;
        string location;
        uint datetime;
        bytes32[] checks;
    }

    bytes32[] public allAssets;
    bytes32[] public allCheckIns;
    mapping(bytes32 => Asset) public  assetMap;
    mapping(bytes32 => CheckIn) public checkInMap;

    function createAsset(bytes32 _id, string memory  _location) public {
        Asset memory newAsset = Asset(_id, msg.sender, _location, block.timestamp,  new bytes32[](0));
        allAssets.push(_id);
        assetMap[_id] = newAsset;
        checkIn(_id,_location, msg.sender);
    }

    function checkIn(bytes32 _id, string memory  _location, address _checker) public {
        bytes32 id = keccak256(abi.encodePacked(_id, _location, _checker, block.timestamp));
        CheckIn memory check = CheckIn(_checker, _location, block.timestamp, _id, id);
        allCheckIns.push(id);
        checkInMap[id] = check;
        assetMap[_id].checks.push(id);
    }
    function getCheckIns(bytes32 _id) view public returns( bytes32[] memory) {
        return assetMap[_id].checks;
    }

    function random() public view returns(bytes32){
         bytes32 id = keccak256(abi.encodePacked( block.timestamp));
         return id;
    }








}
