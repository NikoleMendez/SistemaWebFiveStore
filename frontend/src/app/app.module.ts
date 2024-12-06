import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { TutorialsService } from './servicios/tutorials.service';
// Importación del componente raíz de la aplicación

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { RouterModule, Routes } from '@angular/router';
import { BaseComponent } from './base/base.component';
import { InicioComponent } from './inicio/inicio.component';
import { LoginComponent } from './login/login.component';
import { PerfilComponent } from './perfil/perfil.component';
import { RegistrarseComponent } from './registrarse/registrarse.component';

@NgModule({

  declarations: [
    AppComponent,
    BaseComponent,
    InicioComponent,
    LoginComponent,
    PerfilComponent,
    RegistrarseComponent

  ],
  imports: [
    
    BrowserModule,
    HttpClientModule,
    //RouterModule,
    AppRoutingModule,
    RouterModule.forRoot([]),
   
    
   
  ],
  providers: [TutorialsService],

  bootstrap: [AppComponent]
})

export class AppModule { }
