# Colombian-license-plate-recognizer
This is a license plate recognizer (ANPR) for Colombian yellow license plates. 
It does work like an usual ANPR except it focuses on yellow plates, therefore being a little bit tricky at the time of localizing the license plate. 
I'm using a variety of images I found on the internet from different quality, ilumination and size, thus the recognizer can't distinguish some of them.

This is how it works.

Let's say we have this picture:



<img src="https://user-images.githubusercontent.com/62145703/178170708-1458edb4-7694-4fc6-823f-7891670c0f3e.png"  width="400"/>

First using opencv we convert to HSV and perform a thresholding operation to mask out the yellow part of the image. We should end up with something like this:

<img src="https://user-images.githubusercontent.com/62145703/178170743-0c913fc9-55b4-40ad-ac6b-30cad274be5d.png"  width="400"/>

Now that the plate has been marked we find the countours of the image and select the biggest one, about 95% of the time it selects the license plate.


<img src="https://user-images.githubusercontent.com/62145703/178172258-12c68d4e-2cd8-4663-a0b3-796f89c87339.png"  width="400"/>

This is the selected and cropped countour:

<img src="https://user-images.githubusercontent.com/62145703/178172532-4bdc387a-c093-4aa1-9550-dada3ad61c93.png"  width="400"/>

Now with the cropped license we can once again find countours and select the ones with an specific area, perimeter and ratio. Usually it selects the characters we're looking for.
After having the separate characters we apply some filters and blur for the OCR to be more accurate.



<p float="left">
  <img src="https://user-images.githubusercontent.com/62145703/178173149-b8f19a2b-6299-4b66-bd29-35d0fd02e2cf.png" width="100" />
  <img src="https://user-images.githubusercontent.com/62145703/178173155-c85cca61-ff90-43ae-a869-8917905dabf0.png" width="100" /> 
  <img src="https://user-images.githubusercontent.com/62145703/178173159-79db7ee4-c109-4688-9dba-d77522984da8.png" width="100" />
  
  <img src="https://user-images.githubusercontent.com/62145703/178173164-8f4e36d6-1097-4d0b-a144-019ad0e80b79.png" width="100" />
  <img src="https://user-images.githubusercontent.com/62145703/178173165-31e0ab52-ed98-4336-b39c-7c461e3ffd71.png" width="100" />
  <img src="https://user-images.githubusercontent.com/62145703/178173167-08c90f66-b5af-4109-92af-451a4d77d939.png" width="100" />
</p>

Now we can use pytesseract to recognize each character from the pictures and we're done!
