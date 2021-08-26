// HADCOINS ICO

pragma solidity >=0.7.0 <0.9.0;

contract hadcoin_ico {
    
    // Introducing the maximum number of hadcoins available for sale
    
    uint public max_hadcoins = 1000000;
    
    // Introducing USD to hadcoins conversion rate

    uint public usd_to_hadcoins = 1000;
    
    // Introducing the total number of hadcoins that have been bought
    uint public total_hadcoins_bought = 0;
    
    // Mapping from investor address to its equity in hadcoins and USD
    
    mapping(address => uint) equity_hadcoins
    mapping(address => uint) equity_usd
    
    // Check if an investor can buy some hadcoins
    modifier can_buy_hadcoins(uint usd_invested) {
        require(usd_invested * usd_to_hadcoins + total_hadcoins_bought < max_hadcoins)
    }
    
    // Getting the equity of an investor in hadcoins
    function equity_in_hadcoins(address investor) external constant return (uint) {
        return equity_hadcoins[investor];
    }
    
    // Getting the equity of an investor in usd
    function equity_in_usd(address investor) external constant return (uint) {
        return equity_usd[investor];
    }
    
    // buying hadcoins
    function buy_hadcoins(address investor, uint usd_invested) external 
    can_buy_hadcoins(usd_invested) {
        equity_hadcoins[investor] += usd_invested * usd_to_hadcoins;
        equity_usd[investor] = equity_hadcoins[investor] / usd_to_hadcoins;
        total_hadcoins_bought += usd_invested * usd_to_hadcoins;
    }
    
    // selling HADCOINS
    function sell_hadcoins(address investor, uint hadcoins_sold) external {
        equity_hadcoins[investor] -= hadcoins_sold;
        equity_usd[investor] = equity_hadcoins[investor] / usd_to_hadcoins;
        total_hadcoins_bought -= hadcoins_sold;
    }
    
}