window.dccFunctions = window.dccFunctions || {};

window.dccFunctions.numberToDate = function(value) {
    //Set starting datae
    const startDate = new Date(Date.UTC(2020, 0, 1)); 
    
    //Have to do this so that it isn't off by 1 day sometimes?
    const oneDayMs = 24 * 60 * 60 * 1000;

    //Get date at index
    const mappedDate = new Date(startDate.getTime() + value * oneDayMs);
    return mappedDate.toISOString().split('T')[0];
};
