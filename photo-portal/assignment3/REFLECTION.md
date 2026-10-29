# Reflection

The slideshow was the requirement I struggled with the most because I had to connect the backend API with the JavaScript in the browser. I understood the individual parts, but getting everything to work together was more challenging. The browser needs to request photos from the `/photos` API, display them, switch images every three seconds, and stop when the user clicks Stop.

One thing I had to pay attention to was how the API returned the photos. Each photo was stored as a JSON string inside the `photos` list instead of an object. This meant the JavaScript had to parse each string before it could get the photo name and create the image path. Otherwise, the API request could work without the slideshow actually displaying anything.

To implement this, I used a fetch request, a function to display the current image, and a timer to switch photos every three seconds. After the last photo, it loops back to the first. I also made sure restarting the slideshow clears the previous timer so multiple timers aren't running at once. The Stop button clears the timer and keeps the current photo displayed.

I checked that the Python and JavaScript files passed their syntax checks, but that doesn't guarantee everything works in the browser. To test it properly, I would upload multiple photos, check that they switch every three seconds, and make sure Stop works. If something wasn't loading, I would use the browser console or network panel to figure out the issue.

Overall, this helped me understand how different parts of a web application need to work together. Even though a slideshow seems simple, there are a lot of small details that matter. It also showed me why testing the actual functionality is just as important as checking for syntax errors.


View this in preview mode to see the images!
## Screenshots

### 1. Slideshow JavaScript Implementation

![\](<Screenshot 2026-10-28 at 11.28.56 PM.png>)
](<Screenshot 2026-10-28 at 11.28.56 PM.png>)
### 2. Working Slideshow

![
](<Screenshot 2026-10-28 at 11.44.00 PM.png>)
### 3. API Response Testing

![](<Screenshot 2026-10-28 at 11.44.58 PM.png>)