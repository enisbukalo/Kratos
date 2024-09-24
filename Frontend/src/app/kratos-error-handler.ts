import { HttpErrorResponse } from "@angular/common/http";
import { throwError } from "rxjs";

export class KratosErrorHandler {
    handleError(error: HttpErrorResponse) {
        if (error.status === 0) {
            console.error('An error occurred:', error.error);
        } else {
            console.error(`Api returned code ${error.status}, body was: `, error.error);
        }
        return throwError(() => `Unknown error occurred:\n${JSON.stringify(error, null, 4)}`);
    }
}