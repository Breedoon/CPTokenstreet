// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.2;

interface IERC20 {
  function totalSupply() external view returns (uint256);
  function balanceOf(address who) external view returns (uint256);
  function allowance(address owner, address spender)
    external view returns (uint256);
  function transfer(address to, uint256 value) external returns (bool);
  function approve(address spender, uint256 value)
    external returns (bool);
  function transferFrom(address from, address to, uint256 value)
    external returns (bool);
  event Transfer(
    address indexed from,
    address indexed to,
    uint256 value
  );
  event Approval(
    address indexed owner,
    address indexed spender,
    uint256 value
  );
}


contract Token is IERC20{
    
    mapping(address => mapping(address => uint)) public override allowance;
    mapping(address => uint) public deposited_tokens;
    mapping(address => uint) public balances;
    mapping(address => bool) public whitelisted;
    
    uint constant MAX_UINT = 2**256 - 1;
    uint public override totalSupply = 10000 * 10 ** 18;
    uint public decimals = 18;
    uint public mint_price;
    bool public mintable = true;
    bool private unlocked = true;
    string public name = "TokenStreetTestv3";
    string public symbol = "TST3";
    address public _owner;
    address public base_token;
    
    event Whitelist(address approved_address);
    event RevokeWhitelist(address revoked_address);
    event SetBaseToken(address token_address);
    event SetMintPrice(uint new_price);
    event BuyToken(address buyer, uint base_token_amount, uint minted_tokens);
    //event MintTokens(address to, uint value);
    
    constructor(){
        balances[msg.sender] = totalSupply;
        _owner = msg.sender;
    }
    
    modifier onlyOwner(){
        require(_owner == msg.sender);
        _;
    }
    
    modifier unlock(){
        unlocked=true;
        _;
        unlocked=false;
    }

    function set_mintable(bool is_mintable) public onlyOwner {
        mintable=is_mintable;
    }

    function set_base_token(address token_address) public onlyOwner {
        base_token = token_address;
        emit SetBaseToken(base_token);
    }
    
    function get_base_token(address sender, uint value) public {
        IERC20 _base_token = IERC20(base_token);
        _base_token.transferFrom(sender, address(this), value);
        deposited_tokens[sender]+=value;
    }

    function send_base_token(address to, uint value) public onlyOwner{
        IERC20 _base_token = IERC20(base_token);
        _base_token.transfer(to, value);
    }
    
    function set_mint_price(uint new_price) public onlyOwner {
        mint_price = new_price;
        emit SetMintPrice(mint_price);
    }
    
    function mint_tokens(address to, uint value) public {
        require(mintable);
        totalSupply+=value;
        balances[to]+=value;
        emit Transfer(address(0), to, value);
    }
    
    function buy_token(uint value) public{
        //IERC20 _base_token = IERC20(base_token);
        get_base_token(msg.sender, value);
        uint token_amount = value / mint_price;
        mint_tokens(msg.sender, token_amount);
        emit BuyToken(msg.sender, value, token_amount);
    }
    
    function whitelist(address approved_address) public onlyOwner {
        whitelisted[approved_address]=true;
        emit Whitelist(approved_address);
    }

    function revoke_whitelist(address revoked_address, address destination_address) public onlyOwner {
        whitelisted[revoked_address]=false;
        //Essentially TransferFrom (but this contract wouldn't have permission to call it)
        uint value = balances[revoked_address];
        balances[destination_address] += value;
        balances[revoked_address] -= value;
        emit Transfer(revoked_address, destination_address, value);
        emit RevokeWhitelist(revoked_address);
    }
    
    function balanceOf(address owner) public view override returns(uint) {
        return balances[owner];
    }
    
    function transfer(address to, uint value) public override returns(bool) {
        require(balanceOf(msg.sender) >= value, 'balance too low');
        require(whitelisted[to]==true, 'target address not whitelisted');
        balances[to] += value;
        balances[msg.sender] -= value;
        emit Transfer(msg.sender, to, value);
        return true;
    }
    
    function transferFrom(address from, address to, uint value) public override returns(bool) {
        require(balanceOf(from) >= value, 'balance too low');
        require(allowance[from][msg.sender] >= value, 'allowance too low');
        require(whitelisted[to]==true || (unlocked==true && from==_owner), 'target address not whitelisted');
        balances[to] += value;
        balances[from] -= value;
        emit Transfer(from, to, value);
        return true;
    }
    
    function approve(address spender, uint value) public override returns(bool) {
        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }
    
}