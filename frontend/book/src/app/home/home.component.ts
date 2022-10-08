import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { RestService } from '../service/rest.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  private fileTmp:any;
  //Form Validables 
  registerForm: any = FormGroup;
  submitted = false;
  constructor(private CS:RestService, private formBuilder: FormBuilder){}
  //Add user form actions
  get f() { return this.registerForm.controls; }
  onSubmit() {
    
    this.submitted = true;
    // stop here if form is invalid
    if (this.registerForm.invalid) {
      return alert("Please choose a PDF file");
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
      words: ''
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

  searchWords(word: string){
    const body = new FormData();
    if(this.fileTmp!=null){
      body.append('file', this.fileTmp.fileRaw);
      body.append('words', word);
    }
    // this.CS.createProduct(body).subscribe();
    // window.location.reload();
  }

}
