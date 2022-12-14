import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { RestService } from '../service/rest.service';

interface Result {
  totalWords: any,
  words: any
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})

export class HomeComponent implements OnInit {
  public loader = ""
  private fileTmp:any;
  //Form Validables 
  registerForm: any = FormGroup;
  public formGroup: FormGroup | any;
  submitted = false;

  constructor(private CS:RestService, private formBuilder: FormBuilder){}

  //Add user form actions
  get f() { return this.registerForm.controls; }

  jsonToFinalResult(json: string){
    let currentWord: string = ""
    let finalString: string = "";
    let specialCharaters = ["{","}",","];

    for (let i = 1; i < json.length; i++) {

      if(specialCharaters.includes(json[i]) && i !=0){
        finalString += currentWord + " times.\n"
        currentWord = ""
      }
      else{
        currentWord += json[i]
      }
    }

    return finalString
  }

  onSubmit() {
    
    this.submitted = true;
    // stop here if form is invalid
    if (this.registerForm.invalid) {
      return alert("Please choose a PDF file");
    }
    //True if all the fields are filled
    if(this.submitted)
    {
      const body = new FormData();
      body.append('book', this.fileTmp.fileRaw);
      body.append('words', this.registerForm.value.myName);
      this.CS.interactBook(body).subscribe(res => {
        const result: Result = JSON.parse(JSON.stringify(res))



        alert("Total words: "+ result.totalWords + "\n" + 
              "Words: \n" +  this.jsonToFinalResult(JSON.stringify(result.words)))
        window.location.reload();
      })

    }
  
  }
  ngOnInit() {
    //Add User form validations
    this.registerForm = this.formBuilder.group({
      imageInput: ['', [Validators.required]],
      myName: new FormControl()
    });
  }
  //file type validation
  onImageChangeFromFile($event:any)
  {
      if ($event.target.files && $event.target.files[0]) {
        let file = $event.target.files[0];
        this.fileTmp = {
          fileRaw:file,
          fileName:file.name
        }
        console.log(file);
          if(file.type == "application/pdf") {
            console.log("correct");
           
          }
          else {
            //call validation
            this.registerForm.reset();
            this.registerForm.controls["imageInput"].setValidators([Validators.required]);
            this.registerForm.get('imageInput').updateValueAndValidity();
          }
      }
  }

}
