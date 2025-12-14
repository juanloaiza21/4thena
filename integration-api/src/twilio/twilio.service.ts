import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import twilio from 'twilio';

@Injectable()
export class TwilioService {
    private twilioClient: twilio.Twilio;

    constructor(private configService: ConfigService) {
        const accountSid = this.configService.get<string>('twilio.accountSid');
        const authToken = this.configService.get<string>('twilio.authToken');

        this.twilioClient = twilio(accountSid, authToken);
    }
}
