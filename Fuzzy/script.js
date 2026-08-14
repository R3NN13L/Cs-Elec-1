const slider = document.getElementById("distance"); 

const distanceValue = document.getElementById("distanceValue"); 

const leftDoor = document.getElementById("leftDoor"); 

const rightDoor = document.getElementById("rightDoor"); 

const near = document.getElementById("near"); 

const medium = document.getElementById("medium"); 

const far = document.getElementById("far"); 

const opening = document.getElementById("opening"); 

const status = document.getElementById("status"); 

const formula = document.getElementById("formula"); 

slider.addEventListener("input", updateDoor); 

updateDoor(); 

function triangular(x, a, b, c) { 
  if (a === b && x === a) { 
    return 1; 
  } 

  if (b === c && x === c) { 
    return 1; 
  } 

  if (x <= a || x >= c) { 
    return 0; 
  } else if (x == b) { 
    return 1; 
  } else if (x > a && x < b) { 
    return (x - a) / (b - a); 
  } else if (x > b && x < c) { 
    return (c - x) / (c - b); 
  } 

  return 0; 
} 

function updateDoor() { 
  let d = Number(slider.value); 

  distanceValue.innerHTML = d + " cm"; 

  let n = triangular(d, 0, 0, 60); 
  let m = triangular(d, 30, 50, 70); 
  let f = triangular(d, 40, 100, 120); 

  n = Number(n.toFixed(2)); 
  m = Number(m.toFixed(2)); 
  f = Number(f.toFixed(2)); 

  near.innerHTML = n; 
  medium.innerHTML = m; 
  far.innerHTML = f; 

  let nearOutput = 100; 
  let mediumOutput = 50; 
  let farOutput = 0; 

  let numerator = n * nearOutput + m * mediumOutput + f * farOutput; 
  let denominator = n + m + f; 

  let open = 0; 

  if (denominator != 0) { 
    open = numerator / denominator; 
  } 

  open = Number(open.toFixed(2)); 

  opening.innerHTML = "Door Opening : " + open + "%"; 

  formula.innerHTML = 
    "Near = " + 
    n + 
    "\nMedium = " + 
    m + 
    "\nFar = " + 
    f + 
    "\n\nTriangular Membership Function" + 
    "\n\nNear Output = 100%" + 
    "\nMedium Output = 50%" + 
    "\nFar Output = 0%" + 
    "\n\nFormula:" + 
    "\n((" + 
    n + 
    "×100)+(" + 
    m + 
    "×50)+(" + 
    f + 
    "×0)) / (" + 
    n + 
    "+" + 
    m + 
    "+" + 
    f + 
    ")" + 
    "\n\nDoor Opening = " + 
    open + 
    "%"; 

  let move = open * 1.4; 

  leftDoor.style.left = -move + "px"; 
  rightDoor.style.right = -move + "px"; 

  if (open < 20) { 
    status.innerHTML = "Door Closed"; 
  } else if (open < 70) { 
    status.innerHTML = "Door Half Open"; 
  } else { 
    status.innerHTML = "Door Fully Open"; 
  } 
}