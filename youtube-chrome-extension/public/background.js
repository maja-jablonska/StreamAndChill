/* eslint-disable no-unused-expressions */
/* eslint-disable no-undef */
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ videoIds: {} });
  console.log("Starting the Youtube&Chill extension")

  chrome.declarativeContent.onPageChanged.removeRules(undefined, () => {
    chrome.declarativeContent.onPageChanged.addRules([
      {
        conditions: [
          new chrome.declarativeContent.PageStateMatcher({
            pageUrl: { hostSuffix: "youtube.com/watch" },
          }),
        ],
        actions: [new chrome.declarativeContent.ShowPageAction()],
      },
    ]);
  });
});

chrome.webNavigation.onHistoryStateUpdated.addListener(() => {
  checkVideoId()
})

chrome.webNavigation.onCompleted.addListener(() => {
  checkVideoId()
})

showOverlay = () => {
  console.log("Created");
  var div = document.createElement("div");
  div.style.width = "100px";
  div.style.height = "100px";
  div.innerHTML = "Hello";
  document.body.appendChild(div);
}

checkVideoId = () => {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    var activeTab = tabs[0];
    var activeTabUrl = activeTab.url; // or do whatever you need
    videoId = youtube_parser(activeTabUrl)
    let videoIds = {}
    chrome.storage.local.get('videoIds', (data) => {
      videoIds = data.videoIds
    });
    if (videoId && (!videoIds[activeTab.id] || videoIds[activeTab.id] != videoId)) {
      videoIds[activeTab.id] = videoId
      chrome.storage.local.set({videoIds: videoIds})
      console.log("Video id: ", videoIds)
      fetchVideoData(videoId)
      // var div = document.createElement("div");
      // div.style.width = "100px";
      // div.style.height = "100px";
      // div.innerHTML = "Hello";
      // document.body.appendChild(div);
      
      // Make request to BE
      console.log("???")
      chrome.scripting.executeScript({
        target: { tabId: activeTab.id },
        func: showOverlay
      });
    //   chrome.tabs.sendMessage(tabs[0].id, {createDiv: {width: "100px", height: "100px", innerHTML: "Hello"}}, function(response) {
    //     console.log(response.confirmation);
    // });
    }
  });
}

fetchVideoData = (videoId) => {
  console.log("Fetching data about video: ", videoId)
  fetch('https://dreamteamzurich.herokuapp.com/' + videoId)
    .then(response => {
      if (response.status !== 200) {
        console.log('Looks like there was a problem. Status Code: ' +
          response.status);
        return;
      }

      // Examine the text in the response
      response.json().then(function(data) {
          console.log("Success!!!", data);
          // TODO: this will work only with 1 youtube tab open at one time
          calmestFragment = chooseCalmestVideoFragment(data)
          if (calmestFragment == null) {
            console.log("Video classified as *not* calm")
          } else {
            console.log("Calm video detected, will start breathing exercise at timestamp: ", calmestFragment)
            chrome.storage.local.set({startTimestamp: calmestFragment})
          }
          
      });
    })
    .catch(function(err) {
      console.log('Fetch Error :-S', err);
    });
}

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  console.log("updated!", changeInfo)
  if (changeInfo.status === "complete" && tab.active) {
    chrome.scripting.executeScript(
      {
        target: {tabId: tabId},
        files: ["content.js"],
      },
      () => {
        const error = chrome.runtime.lastError;
        if (error) "Error. Tab ID: " + tab.id + ": " + JSON.stringify(error);

        chrome.tabs.sendMessage(tabId, {
          requested: "getCurrentTime",
          tabId: tabId
        });
      }
    );
  }
});

function youtube_parser(url){
  var regExp = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
  var match = url.match(regExp);
  if (match && match[2].length == 11) {
    return match[2];
  } else {
    return false
  }
}

chooseCalmestVideoFragment = (data) => {
  // Currently we make decision when and if start breathing exercise 
  // based on simple thresholds that we estimated empirically, in the 
  // future this could be replaced with a trained classifier
  if (data.aggresive) {
    return null
  }
  fragmentsToConsider = []
  data.timestamps.forEach(t => {
    // discard fragments with high BPM, high avg_db_deviation or high dancebility
    if (!(t.bpm > 130 || t.avg_db_deviation > -15 || t.danceability > 1.25)) {
      fragmentsToConsider = [...fragmentsToConsider, t.start]
    }
  })
  if (fragmentsToConsider.length === 0) {
    return null
  }
  // normally we would normalize the data and choose the calmest fragment based on it
  // but out of lack of time let's just do it randomly for now
  return fragmentsToConsider[Math.floor(Math.random() * fragmentsToConsider.length)]
}
