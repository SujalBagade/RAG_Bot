In India, an NDA (Non-Disclosure Agreement) is a legal contract that protects confidential information shared between parties. Here's a general process for creating an NDA in India:

Identify Parties: Clearly identify the parties involved in the agreement. Typically, there's a Disclosing Party (the one sharing confidential information) and a Receiving Party (the one receiving and agreeing to keep the information confidential).

Define Confidential Information: Specify what information is considered confidential. This could include trade secrets, business plans, financial information, technical data, customer lists, etc. 

Duration of Agreement: Determine the duration for which the agreement will be valid. NDAs often have a defined term during which the information must be kept confidential and may include provisions for how long confidentiality obligations continue after the termination of the agreement. 

Exclusions: Define what information is not considered confidential. This may include information that is already in the public domain or becomes public through no fault of the Receiving Party. 

Obligations of Receiving Party: Clearly outline the obligations of the Receiving Party regarding the confidential information. This typically includes clauses specifying that the Receiving Party will keep the information confidential, use it only for the intended purpose, and not disclose it to any third parties without prior written consent.

Permitted Disclosures: Specify any circumstances under which the Receiving Party is permitted or required to disclose the confidential information, such as to legal advisors or as required by law. 

Remedies for Breach: Outline the remedies available in case of a breach of the agreement. This may include injunctions, damages, or other legal remedies.

Governing Law and Jurisdiction: Specify the governing law that will apply to the agreement and the jurisdiction where disputes will be resolved. In India, this is usually governed by Indian law, and the courts of a specific jurisdiction (such as the courts in the city where the agreement was signed) may have jurisdiction over disputes.

Execution and Signatures: Once the terms are finalized, the agreement should be signed by authorized representatives of both parties. It's essential to ensure that all parties understand the terms and voluntarily consent to them.

Retention and Enforcement: Keep copies of the signed agreement for the records of both parties. If necessary, seek legal advice to enforce the agreement in case of a breach.

It's important to note that while this provides a general overview of the process, creating an NDA may require customization based on the specific circumstances and requirements of the parties involved. It's advisable to consult with a qualified legal professional experienced in drafting NDAs to ensure that the agreement adequately protects the interests of all parties involved and complies with applicable laws and regulations in India.

 1. An NDA (Non-Disclosure Agreement) is a legal contract that protects confidential information shared between parties in India.

2. Parties involved in an NDA typically include a Disclosing Party (the one sharing confidential information) and a Receiving Party (the one receiving and agreeing to keep the information confidential).

3. The confidential information covered in an NDA can include trade secrets, business plans, financial information, technical data, customer lists, and more.

4. The duration of an NDA is determined by the parties involved, with provisions for how long confidentiality obligations continue after the termination of the agreement.

5. It is important to clearly define what information is not considered confidential in an NDA, such as information already in the public domain or becomes public through no fault of the Receiving Party.

6. The obligations of the Receiving Party in an NDA typically include clauses specifying that the information must be kept confidential, used only for the intended purpose, and not disclosed to third parties without prior written consent.

7. Permitted disclosures in an NDA specify circumstances under which the Receiving Party is allowed or required to disclose the confidential information, such as to legal advisors or as required by law.

8. Remedies for breach of an NDA may include injunctions, damages, or other legal remedies to protect the interests of the parties involved.

9. The governing law and jurisdiction of an NDA in India are usually governed by Indian law, with disputes resolved in the courts of a specific jurisdiction, such as the courts in the city where the agreement was signed.

10. It is advisable to consult with a qualified legal professional experienced in drafting NDAs to ensure that the agreement adequately protects the interests of all parties involved and complies with applicable laws and regulations in India.

CSR: In public key infrastructure (PKI) systems, a certificate signing request (CSR or certification request) is a message sent from an applicant to a certificate authority of the public key infrastructure (PKI) in order to apply for a digital identity certificate. The CSR usually contains the public key for which the certificate should be issued, identifying information (such as a domain name) and a proof of authenticity including integrity protection (e.g., a digital signature). The most common format for CSRs is the PKCS #10 specification; others include the more capable Certificate Request Message Format (CRMF)[1] and the SPKAC (Signed Public Key and Challenge) format generated by some web browsers.
Certificate signing request

Article
Talk
Read
Edit
View history

Tools
From Wikipedia, the free encyclopedia
In public key infrastructure (PKI) systems, a certificate signing request (CSR or certification request) is a message sent from an applicant to a certificate authority of the public key infrastructure (PKI) in order to apply for a digital identity certificate. The CSR usually contains the public key for which the certificate should be issued, identifying information (such as a domain name) and a proof of authenticity including integrity protection (e.g., a digital signature). The most common format for CSRs is the PKCS #10 specification; others include the more capable Certificate Request Message Format (CRMF)[1] and the SPKAC (Signed Public Key and Challenge) format generated by some web browsers.

Procedure
Before creating a CSR for an X.509 certificate, the applicant first generates a key pair, keeping the private key of that pair secret. The CSR contains information identifying the applicant (such as a distinguished name), the public key chosen by the applicant, and possibly further information. When using the PKCS #10 format, the request must be self-signed using the applicant's private key, which provides proof-of-possession of the private key but limits the use of this format to keys that can be used for (some form of) signing. The CSR should be accompanied by a proof of origin (i.e., proof of identity of the applicant) that is required by the certificate authority, and the certificate authority may contact the applicant for further information.

Typical information required in a CSR (sample column from sample X.509 certificate). Note that there are often alternatives for the Distinguished Names (DN), the preferred value is listed.
A certification request in PKCS #10 format consists of three main parts: the certification request information, a signature algorithm identifier, and a digital signature on the certification request information. The first part contains the significant information, including the public key. The signature by the requester prevents an entity from requesting a bogus certificate of someone else's public key.[3] Thus the private key is needed to produce a PKCS #10 CSR, but it is not part of, the CSR.[4]

CSR for personal ID certificates and signing certificates must have the email address of the ID holder or name of organisation in case of business ID.

The first part, ASN.1 type CertificationRequestInfo, consists of a version number (which is 0 for all known versions, 1.0, 1.5, and 1.7 of the specifications), the subject name, the public key (algorithm identifier + bit string), and a collection of attributes providing additional information about the subject of the certificate. The attributes can contain required certificate extensions, a challenge-password to restrict revocatio

ns, as well as any additional information about the subject of the certificate, possibly including local or future types.[3]

