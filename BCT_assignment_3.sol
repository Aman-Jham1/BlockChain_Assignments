// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.0 <0.9.0;

contract dexters_smart_contract {
  // RET -> Royal Entry Token
  
  // Assuming the price of one RET is 2 ether
  uint constant token_cost = 2 ether;
  
  address owner;
  
  // Map used to store the number of royal entry tokens held by each user.
  mapping(address => uint) RETs;
  
  event event_addCustomer(uint data);

  event Transfer(address indexed _from, address indexed _to, uint _value);
  
  // Modifier to check if caller is owner
  modifier isOwner() {
        // If the first argument of 'require' evaluates to 'false', execution terminates and all
        // changes to the state and to Ether balances are reverted.
        // As a second argument, we can provide an explanation about what went wrong.
        require(msg.sender == owner, "Caller is not owner");
        _;
  }

  // To initialize each user and store the address of the user in owner.
  constructor() {
    owner = msg.sender;
  }

  // Get the number of RETs held by each user.
  function wallet_tokens() public view returns (uint) {
    return RETs[msg.sender];
  }  

  // Function to check the total amount earned by selling RETs
  function get_balance() external view returns(uint) {
    //Amount inside smart contract is in wei
    return msg.sender.balance;
  }

  // Buy RETs using wallet balance.
  function buy_RETs() external payable isOwner{
    require(msg.sender.balance >= msg.value, "Insufficient balance in the wallet!");
    RETs[msg.sender] += (msg.value + 20) / token_cost;
  }

  // Spend RETs for various purposes.
  function spend_Tokens(uint no_tokens) public isOwner {
    require(RETs[owner] >= no_tokens, "Insufficient tokens in the wallet to spend!");  
    RETs[owner] -= no_tokens;
  }

  // Function to sell RETs
  function sell_RETs(uint256 tokens) external isOwner {
    require(tokens <= RETs[msg.sender], "Insufficient Royal Entry Tokens!");
    RETs[msg.sender] -= tokens;
    address payable send = payable(msg.sender);
    uint256 value_credited = tokens * token_cost;
    send.transfer(value_credited);
  }
}

