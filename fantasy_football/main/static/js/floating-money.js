// document.addEventListener('DOMContentLoaded', function () {
//   if (window.location.pathname === '/') {
//     // Hard-coded offsets for header & footer
//     const HEADER_HEIGHT = 131;
//     const FOOTER_HEIGHT = 55;

//     // We'll treat the entire viewport as the container for bounding.
//     const containerWidth = window.innerWidth;
//     const containerHeight = window.innerHeight;

//     const moneySize = 30; // approximate size (px) of your '$' element

//     function createMoneySign() {
//       const moneySign = document.createElement('span');
//       moneySign.classList.add('money');
//       moneySign.textContent = '$';
//       document.body.appendChild(moneySign); 
//       // ^ Directly appending to <body>. (Or you can still append to #floating-money
//       //   if you prefer, but be aware it might overlap. The bounding logic won't care.)

//       // We'll pick a random X between 0 and containerWidth
//       // We'll pick a random Y between HEADER_HEIGHT and containerHeight - FOOTER_HEIGHT
//       let x = Math.random() * (containerWidth - moneySize);
//       let y = HEADER_HEIGHT + Math.random() * ((containerHeight - HEADER_HEIGHT - FOOTER_HEIGHT) - moneySize);

//       // Speeds
//       let xSpeed = Math.random() * 2 + 1;
//       let ySpeed = Math.random() * 2 + 1;

//       function move() {
//         x += xSpeed;
//         y += ySpeed;

//         // Bounce if hitting the left or right edges
//         if (x <= 0 || x >= (containerWidth - moneySize)) {
//           xSpeed = -xSpeed;
//         }

//         // Bounce if hitting the "top boundary" = header's bottom, or the "bottom boundary" = top of footer
//         // which is containerHeight - FOOTER_HEIGHT
//         if (y <= HEADER_HEIGHT || y >= (containerHeight - FOOTER_HEIGHT - moneySize)) {
//           ySpeed = -ySpeed;
//         }

//         moneySign.style.transform = translate(${x}px, ${y}px) translate(-50%, -50%);
//         requestAnimationFrame(move);
//       }

//       move();
//     }

//     // Create multiple '$' signs
//     for (let i = 0; i < 100; i++) {
//       createMoneySign();
//     }
//   }
// });
document.addEventListener('DOMContentLoaded', function () {
  if (window.location.pathname === '/minigame/') {
    const HEADER_HEIGHT = 185;
    const FOOTER_HEIGHT = 55;
    const containerWidth = window.innerWidth;
    const containerHeight = window.innerHeight;

    const moneySize = 30; // Size of the dollar sign element

    const floatingMoneyContainer = document.getElementById('floating-money');
    if (!floatingMoneyContainer) {
      // Create a container if it doesn't exist
      const container = document.createElement('div');
      container.id = 'floating-money';
      container.style.position = 'fixed';
      container.style.top = '0';
      container.style.left = '0';
      container.style.width = '100vw';
      container.style.height = '100vh';
      container.style.pointerEvents = 'none';
      container.style.zIndex = '9999';
      document.body.appendChild(container);
    }

    // Array to hold all the floating dollar signs
    let moneySigns = [];

    // Function to create and animate each dollar sign
    function createMoneySign() {
      const moneySign = document.createElement('span');
      moneySign.classList.add('money');
      moneySign.textContent = '$';
      floatingMoneyContainer.appendChild(moneySign);

      // Random start position
      let x = Math.random() * (containerWidth - moneySize);
      let y = HEADER_HEIGHT + Math.random() * (containerHeight - HEADER_HEIGHT - FOOTER_HEIGHT - moneySize);

      // Random speed
      let xSpeed = Math.random() * 2 + 1;
      let ySpeed = Math.random() * 2 + 1;

      // Store position, speed, and state for later reference
      moneySign.x = x;
      moneySign.y = y;
      moneySign.xSpeed = xSpeed;
      moneySign.ySpeed = ySpeed;
      moneySign.moving = true; // Initially moving

      // Movement function
      function move() {
        if (!moneySign.moving) return; // Skip movement if "swimming" away

        moneySign.x += moneySign.xSpeed;
        moneySign.y += moneySign.ySpeed;

        // Bounce off the walls (with proper bounds)
        if (moneySign.x <= 0 || moneySign.x >= (containerWidth - moneySize)) {
          moneySign.xSpeed = -moneySign.xSpeed;
        }

        if (moneySign.y <= HEADER_HEIGHT || moneySign.y >= (containerHeight - FOOTER_HEIGHT - moneySize)) {
          moneySign.ySpeed = -moneySign.ySpeed;
        }

        // Apply the transform to the dollar sign
        moneySign.style.transform = `translate(${moneySign.x}px, ${moneySign.y}px) translate(-50%, -50%)`;

        requestAnimationFrame(move);
      }

      move();
      moneySigns.push(moneySign); // Add the sign to the array
    }

    // Create 100 dollar signs
    for (let i = 0; i < 100; i++) {
      createMoneySign();
    }

    // Handle mouse click events (touchpad press should also trigger click)
    document.addEventListener('click', function (event) {
      const mouseX = event.clientX;
      const mouseY = event.clientY;
      console.log("Mouse clicked at", mouseX, mouseY); // Debugging click location

      // Check if the mouse is near any of the dollar signs and make them swim away
      moneySigns.forEach(function (sign) {
        const distance = Math.sqrt(Math.pow(sign.x - mouseX, 2) + Math.pow(sign.y - mouseY, 2));

        if (distance < 150) { // You can adjust this distance to your liking
          const angle = Math.atan2(sign.y - mouseY, sign.x - mouseX);
          const swimSpeed = 50; // Speed at which the dollar signs swim away

          // Temporarily disable normal movement
          sign.moving = false;

          // Move the sign away from the click
          sign.x += Math.cos(angle) * swimSpeed;
          sign.y += Math.sin(angle) * swimSpeed;

          // Reset the sign to resume normal movement after 500ms
          setTimeout(function () {
            sign.moving = true;
          }, 500); // Reset after 500ms
        }
      });
    });
  }
});

