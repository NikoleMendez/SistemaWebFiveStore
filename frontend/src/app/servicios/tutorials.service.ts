import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TutorialsService {
  api_url = "http://localhost:8000";

  constructor(private http: HttpClient ) { }

  getMessage(): Observable<any> {
    // Aquí realizamos una solicitud GET a una URL específica en tu servidor
    return this.http.get<any>(`${this.api_url}/profile`);
  }
}
