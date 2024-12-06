import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Importa los componentes que se utilizarán en las rutas
import { InicioComponent } from './inicio/inicio.component';
import { BaseComponent } from './base/base.component'; 
import { LoginComponent } from './login/login.component';
import { PerfilComponent } from './perfil/perfil.component';
import { RegistrarseComponent } from './registrarse/registrarse.component';
import { TutorialsService } from './servicios/tutorials.service';

// Define las rutas de la aplicación
const routes: Routes = [
  { path: '', component: InicioComponent },
  { 
    path: 'base', 
    component: BaseComponent },
  { 
    path: 'login', 
    component: LoginComponent },
  { 
    path: 'mensaje', 
    component: PerfilComponent },
  
  { path: 'registrarse', component: RegistrarseComponent },
 // { path: 'servicios', component: TutorialsService },
  // Otras rutas si las tienes
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
