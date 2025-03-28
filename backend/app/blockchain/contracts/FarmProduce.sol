// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract FarmProduce {
    struct Produce {
        string farmerName;
        string cropName;
        uint256 quantity; // Quantity in kg
        string location;
    }

    mapping(uint256 => Produce) public produces; // Mapping ID to produce details
    uint256 public produceCount = 0; // Counter for unique IDs

    event ProduceAdded(uint256 id);

    // Add produce details
    function addProduce(
        string memory _farmerName,
        string memory _cropName,
        uint256 _quantity,
        string memory _location
    ) public {
        produceCount++;
        produces[produceCount] = Produce(_farmerName, _cropName, _quantity, _location);
        emit ProduceAdded(produceCount);
    }

    // Get produce details by ID
    function getProduce(uint256 _id)
        public
        view
        returns (
            string memory,
            string memory,
            uint256,
            string memory
        )
    {
        Produce memory produce = produces[_id];
        require(bytes(produce.farmerName).length > 0, "Produce does not exist");
        return (produce.farmerName, produce.cropName, produce.quantity, produce.location);
    }

    // Get all produce details
    function getAllProduces() public view returns (string[] memory, string[] memory, uint256[] memory, string[] memory) {
        string[] memory farmerNames = new string[](produceCount);
        string[] memory cropNames = new string[](produceCount);
        uint256[] memory quantities = new uint256[](produceCount);
        string[] memory locations = new string[](produceCount);

        for (uint256 i = 1; i <= produceCount; i++) {
            Produce memory produce = produces[i];
            farmerNames[i - 1] = produce.farmerName;
            cropNames[i - 1] = produce.cropName;
            quantities[i - 1] = produce.quantity;
            locations[i - 1] = produce.location;
        }

        return (farmerNames, cropNames, quantities, locations);
    }
}