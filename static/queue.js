const body = document.querySelector("body");
const testVideo = document.querySelector("#test-video");
const scoreContainer = document.querySelector(".background-container");
let showVideo = false;
testVideo.style.display = "none";
let startTime = new Date();

HOST = "192.168.76.152";
PORT = 2207;

const scoreList = document.querySelector(".score-list");

class BalloonScore {
    constructor(id) {
        this.id = id;
        this.points = 0;
        this.rank = id;
        this.htmlElement = document.querySelector(`#balloon${id}`);
    }
}

let daily_record = 0;
let season_record = 0;

// instantiate the 12 score objects
let balloonScores = [];
for (let id=1; id<13; id++) {
    let ballonScore = new BalloonScore(id);
    balloonScores.push(ballonScore);
};

document.addEventListener('DOMContentLoaded', () => {
    const fetchData = async () => {
        try {
            // check time difference for switch between video and score
            let now = new Date();
            let timeDiff = (now - startTime) / 1000;
            if (timeDiff > 30) {
                showVideo = !showVideo;
                startTime = now;
            };

            if (!showVideo) {
                testVideo.pause(); 
                testVideo.currentTime = 0;
                testVideo.style.display = "none";
                scoreContainer.style.display = "block";
            } else {
                scoreContainer.style.display = "none";
                testVideo.style.display = "block";
                testVideo.play();
            }
            
            const response = await fetch('/score_data');
            if (!response.ok) {
                throw new Error('Netzwerkantwort war nicht ok');
            }
            let score_data = await response.json();
            
            console.log("\nNEW DATA")
            // get list of points for each balloon and assign it to corresponding Score Object
            console.log(score_data);
            for (let i=0; i<12; i++) {
                balloonScores[i].points = score_data[i]
            }
            // sort and rank the objects
            let balloonScoresSorted = balloonScores.slice().sort((score_a, score_b) => score_b.points - score_a.points);
            for (let i=0; i<12; i++) {
                balloonScoresSorted[i].rank = i+1;
            }
            for (let i=0; i<12; i++) {
                console.log(`ID: ${balloonScoresSorted[i].id}`);
                console.log(`Rank: ${balloonScoresSorted[i].rank}`);
                console.log(`Points: ${balloonScoresSorted[i].points}`);
            }
            
            // update frontend
            scoreList.innerHTML = "";
            for (let i=0; i<12; i++) {
                let balloon = balloonScoresSorted[i];
                updateHtmlElement(balloon);
                scoreList.appendChild(balloon.htmlElement)
            } 

            // updated highscore-records
            daily_record = score_data[12];
            season_record = score_data[13];
            document.querySelector("#tagesrekord").innerHTML = daily_record;
            document.querySelector("#jahresrekord").innerHTML = season_record;
        
        } catch (error) {
            console.error('Fehler beim Abrufen der Daten:', error);
        }
    };

    // Daten alle 2 Sekunden abrufen
    setInterval(fetchData, 1000);
});


function updateHtmlElement(balloon) {
    // Structure of an balloonHtmlElement:
    //<div id="balloon1" class="balloon">
    //    <div id="id1" class="id">01</div>
    //    <div id="score1" class="score">001</div>
    //</div>

    balloon.htmlElement.innerHTML = "";
    
    let idDiv = document.createElement("div");
    idDiv.id = `id${balloon.rank}`;
    idDiv.classList.add("id");
    idDiv.innerHTML = balloon.id;

    let scoreDiv = document.createElement("div");
    scoreDiv.id = `score${balloon.rank}`
    scoreDiv.classList.add("score")
    scoreDiv.innerHTML = balloon.points

    balloon.htmlElement.appendChild(idDiv);
    balloon.htmlElement.appendChild(scoreDiv);

    if (balloon.rank == 1) {
        updateWinnerElement(balloon);
    };
}


function updateWinnerElement(balloon) {
    
    let winnerElement = document.createElement("div")
    winnerElement.id = "balloon0";
    winnerElement.classList.add("balloon");
    
    let idDiv = document.createElement("div");
    idDiv.id = `id0`;
    idDiv.classList.add("id");
    idDiv.innerHTML = balloon.id;

    let scoreDiv = document.createElement("div");
    scoreDiv.id = `score0`
    scoreDiv.classList.add("score")
    scoreDiv.innerHTML = balloon.points

    winnerElement.appendChild(idDiv);
    winnerElement.appendChild(scoreDiv);

    scoreList.appendChild(winnerElement);
}

// just for testing ranking mechanism
/*
let testElement = document.querySelector("#balloon1");
testElement.addEventListener("click", () => {    
    //create artificial random balloon Scores
    for (let i=0; i<12; i++) {
        balloonScores[i].points = Math.floor(Math.random() * 1000);
    }
    
    // sort and rank the objects
    let balloonScoresSorted = balloonScores.slice().sort((score_a, score_b) => score_b.points - score_a.points);
    for (let i=0; i<12; i++) {
        balloonScoresSorted[i].rank = i+1;
    }

    for (let i=0; i<12; i++) {
        console.log(`ID: ${balloonScoresSorted[i].id}`);
        console.log(`Rank: ${balloonScoresSorted[i].rank}`);
        console.log(`Points: ${balloonScoresSorted[i].points}`);
    }

    // update frontend
    scoreList.innerHTML = "";
    for (let i=0; i<12; i++) {
        let balloon = balloonScoresSorted[i];
        updateHtmlElement(balloon);
        scoreList.appendChild(balloon.htmlElement)
    } 
});
*/
