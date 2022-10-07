import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  //Form Validables 
registerForm: any = FormGroup;
submitted = false;
constructor( private formBuilder: FormBuilder){}
//Add user form actions
get f() { return this.registerForm.controls; }
onSubmit() {
  
  this.submitted = true;
  // stop here if form is invalid
  if (this.registerForm.invalid) {
      return;
  }
  //True if all the fields are filled
  if(this.submitted)
  {
    alert("Great!!");
  }
 
}
  ngOnInit() {
    //Add User form validations
    this.registerForm = this.formBuilder.group({
      imageInput: ['', [Validators.required]],
 
    });
  }
  //file type validation
  onImageChangeFromFile($event:any)
  {
      if ($event.target.files && $event.target.files[0]) {
        let file = $event.target.files[0];
        console.log(file);
          if(file.type == "image/jpeg") {
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
  // private fileTmp:any;
  // photoName1 = "Choose Photo"

  // constructor() { }

  // ngOnInit(): void {
  // }

  // getFile($event: any): void {
  //   const [ file ] = $event.target.files;
  //   this.fileTmp = {
  //     fileRaw:file,
  //     fileName:file.name
  //   }
  //   this.photoName1 = this.fileTmp.fileName
  // }

}
