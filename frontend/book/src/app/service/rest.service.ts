import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RestService {

  constructor(private http: HttpClient) { }

  interactBook(body:FormData):Observable<any>{
    return this.http.post('http://127.0.0.1:5000/book', body)
  }

}
